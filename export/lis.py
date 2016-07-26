import re
import pymssql
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from tabulate import tabulate

from microbiome.apps.mb_lab.models.maternal_requisition import MaternalRequisition
from microbiome.apps.mb_lab.models.infant_requisition import InfantRequisition

from .lis_credentials import LisCredentials
from .requisition import Requisition
from .utils import undash


class Lis(object):

    """Fetch results from BHP LIS

    For example:

        lis = Lis('BHP071', subject_type='maternal')
        lis.results

    """

    def __init__(self, protocol, df=pd.DataFrame(), subject_type=None, engine=None, protocol_prefix=None):
        self.subject_type = subject_type or 'maternal'
        if not df.empty:
            self.results = df
        else:
            lis_credentials = LisCredentials()
            self.engine = engine or create_engine('mssql+pymssql://{user}:{passwd}@{host}:{port}/{db}'.format(
                user=lis_credentials.username, passwd=lis_credentials.password,
                host=lis_credentials.host, port=lis_credentials.port,
                db=lis_credentials.db))
            self.protocol = protocol
            self.protocol_prefix = protocol_prefix or self.protocol[-3:]
            self.results = self.fetch_results_as_dataframe()
            if self.subject_type == 'maternal':
                self.requisition = Requisition(MaternalRequisition, subject_type=self.subject_type).dataframe
            elif self.subject_type == 'infant':
                self.requisition = Requisition(InfantRequisition, subject_type=self.subject_type).dataframe
            self.update_requisition_columns()

    def print_df(self, df, headers):
        print(tabulate(df, headers=headers, tablefmt='psql'))

    def fetch_results_as_dataframe(self, edc_panels=None):
        with self.engine.connect() as conn, conn.begin():
            df = pd.read_sql_query(self.sql_results, conn)
        df.fillna(value=np.nan, inplace=True)
        df['result'] = df['result'].str.replace('<', '')
        df['result'] = df['result'].str.replace('>', '')
        df['result'] = df['result'].str.replace('*', '')
        df['result'] = df['result'].str.replace('=', '')
        df['result'] = df.apply(
            lambda row: np.nan if row['result'] == '' else row['result'], axis=1)
        # df['result_float'] = df[df['result'].str.contains('\d+')]['result'].astype(float, na=False)
        for column in list(df.select_dtypes(include=['datetime64[ns, UTC]']).columns):
            df[column] = df[column].astype('datetime64[ns]')
        df['result_datetime'] = pd.to_datetime(df['result_datetime'])
        df['received_datetime'] = pd.to_datetime(df['received_datetime'])
        df['drawn_datetime'] = pd.to_datetime(df['drawn_datetime'])
        df['drawn_datetime'] = pd.to_datetime(df['drawn_datetime'].dt.date)
        df['specimen_identifier'] = df.apply(lambda row: np.nan if row['specimen_identifier'] == 'NA' else row['specimen_identifier'], axis=1)
        df['aliquot_identifier'] = df.apply(lambda row: self.aliquot_identifier(row), axis=1)
        df['edc_specimen_identifier'] = df.apply(lambda row: self.edc_specimen_identifier(row, self.protocol_prefix), axis=1)
        df['subject_identifier'] = df.apply(lambda row: undash(row['subject_identifier'], '^{}-'.format(self.protocol_prefix)), axis=1)
        return df

    @property
    def sql_results(self):
        return """select L.PID as lis_identifier, pat_id as subject_identifier,
        edc_specimen_identifier as specimen_identifier, sample_date_drawn as drawn_datetime,
        l.tid as test_id, l.headerdate as received_datetime,
        L21D.utestid, L21D.result, L21D.result_quantifier, L21D.sample_assay_date as result_datetime,
        sample_condition
        from BHPLAB.DBO.LAB01Response as L
        left join BHPLAB.DBO.LAB21Response as L21 ON L21.PID=L.PID
        left join BHPLAB.DBO.LAB21ResponseQ001X0 as L21D on L21D.QID1X0=L21.Q001X0
        where sample_protocolnumber='{}'""".format(self.protocol)

    @property
    def sql_getresults(self):
        return """SELECT * FROM "getresults_dst_history"""

    def update_requisition_columns(self):
        columns = ['edc_specimen_identifier', 'visit_code',
                   'drawn_datetime', 'requisition_datetime', 'is_drawn',
                   'requisition_source']
        self.results = pd.merge(
            self.results,
            self.requisition[pd.notnull(self.requisition['edc_specimen_identifier'])][columns],
            on='edc_specimen_identifier',
            how='left', suffixes=['', '_edc'])
        self.results['requisition_datetime'] = pd.to_datetime(self.results['requisition_datetime'].dt.date)

    def update_edc_specimen_identifier_from_requisition(self, edc_panels=None):
        edc_panels = edc_panels or {'610': 1, '401': 2, '974': 3, '201': 4, '101': 5}
        self.results['edc_panel_id'] = self.results.apply(
            lambda row: edc_panels.get(row['test_id'], 0) if pd.notnull(row['test_id']) else np.nan,
            axis=1)
        df_req = self.requisition[pd.notnull(self.requisition['edc_specimen_identifier'])].copy()
        df_req['requisition_datetime'] = pd.to_datetime(df_req['requisition_datetime'].dt.date)
        df_req = df_req[
            ~(df_req['edc_specimen_identifier'].isin(
                self.results['edc_specimen_identifier']))]
        panel_ids = [1, 3, 4, 5, 2]
        for panel_id in panel_ids:
            self.results = pd.merge(
                self.results,
                df_req[df_req['panel_id'] == panel_id][
                    ['edc_specimen_identifier', 'subject_identifier', 'requisition_datetime',
                     'panel_id']],
                how='left',
                left_on=['final_subject_identifier', 'drawn_datetime', 'edc_panel_id'],
                right_on=['subject_identifier', 'requisition_datetime', 'panel_id'],
                suffixes=['', '_merge'])
            self.results['edc_specimen_identifier'] = self.results.apply(
                lambda row: self.fill_edc_specimen_identifier(row), axis=1)
            self.results.drop(
                ['edc_specimen_identifier_merge', 'subject_identifier_merge',
                 'panel_id', 'requisition_datetime'],
                axis=1, inplace=True)

    def update_final_subject_identifier(self, suffix=None, drop_column=None):
        suffix = suffix or '_edc'
        drop_column = True if drop_column is None else drop_column
        self.results['final_subject_identifier'] = self.results.apply(
            lambda row: self.fill_final_subject_identifier(row, suffix=suffix), axis=1)
        if drop_column:
            del self.results['subject_identifier{}'.format(suffix)]

    def fill_final_subject_identifier(self, row, suffix=None):
        suffix = suffix or '_edc'
        final_subject_identifier = row['final_subject_identifier']
        if pd.isnull(row['final_subject_identifier']):
            if pd.notnull(row['subject_identifier{}'.format(suffix)]):
                final_subject_identifier = row['subject_identifier{}'.format(suffix)]
        return final_subject_identifier

    def fill_edc_specimen_identifier(self, row):
        if (pd.isnull(row['edc_specimen_identifier']) and
                pd.notnull(row['edc_specimen_identifier_merge'])):
            return row['edc_specimen_identifier_merge']
        return row['edc_specimen_identifier']

    def edc_specimen_identifier(self, row, prefix):
        edc_specimen_identifier = np.nan
        if pd.notnull(row['aliquot_identifier']):
            edc_specimen_identifier = row['aliquot_identifier'][0:12]
        elif pd.notnull(row['specimen_identifier']):
            if row['specimen_identifier'].startswith(prefix):
                edc_specimen_identifier = row['specimen_identifier']
        return edc_specimen_identifier

    def aliquot_identifier(self, row):
        aliquot_identifier = np.nan
        for column in ['lis_identifier', 'specimen_identifier']:
            if pd.notnull(row[column]):
                if re.match('^{}\w+[0-9]{{4}}$'.format(self.protocol_prefix), row[column]):
                    aliquot_identifier = row[column]
                    break
        return aliquot_identifier
