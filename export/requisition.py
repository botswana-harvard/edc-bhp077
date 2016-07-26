import pymssql
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from tabulate import tabulate


class Requisition(object):

    def __init__(self, model, subject_type):
        self.subject = self.requisition_df(model, '{}_visit'.format(subject_type))
        self.subject['requisition_source'] = subject_type
        columns = ['subject_identifier', 'edc_specimen_identifier',
                   'visit_code', 'drawn_datetime', 'requisition_identifier',
                   'requisition_datetime', 'is_drawn', 'panel_id', 'requisition_source']
        self.dataframe = self.subject[columns]

    def not_drawn_with_edc_specimen_identifier(self, format=None):
        columns = ['subject_identifier', 'edc_specimen_identifier', 'requisition_identifier']
        df = self.all[pd.notnull(self.all['edc_specimen_identifier']) & ~(self.drawn(self.all))][columns]
        if format == 'dataframe':
            return df
        else:
            print(tabulate(df[columns].sort_values('subject_identifier'),
                           headers=columns, tablefmt='psql'))

    def drawn(self, df):
        return ~df['requisition_identifier'].str.contains(
            '[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}')

    def requisition_df(self, model, visit_model_name):
        qs = model.objects.all()
        columns = qs[0].__dict__.keys()
        columns = self.remove_sys_columns(columns)
        columns.remove('subject_identifier')
        columns.append('{}__appointment__visit_definition__code'.format(visit_model_name))
        columns.append('{}__appointment__registered_subject__subject_identifier'.format(visit_model_name))
        qs = model.objects.values_list(*columns).all()
        df_req = pd.DataFrame(list(qs), columns=columns)
        df_req.rename(columns={
            'specimen_identifier': 'edc_specimen_identifier',
            '{}__appointment__visit_definition__code'.format(visit_model_name): 'visit_code',
            '{}__appointment__registered_subject__subject_identifier'.format(visit_model_name): 'subject_identifier'
        }, inplace=True)
        df_req.fillna(value=np.nan, inplace=True)
        for column in list(df_req.select_dtypes(include=['datetime64[ns, UTC]']).columns):
            df_req[column] = df_req[column].astype('datetime64[ns]')
        return df_req

    def remove_sys_columns(self, columns):
        names = ['_state', '_user_container_instance', 'using']
        for name in names:
            try:
                columns.remove(name)
            except ValueError:
                pass
        return columns
