import os
import pandas as pd

from datetime import date

from edc_model_to_dataframe import EdcModelToDataFrame


class ExportModel:

    def __init__(self, model, consent_model, visit_lookup=None):
        self.add_columns_for = visit_lookup or 'registered_subject'
        self.visit_lookup = visit_lookup
        self.df = pd.DataFrame()
        self.columns = []
        self.model = model
        self.consent_model = consent_model
        self.csv_filename = os.path.expanduser('~/{}_{}_{}.csv'.format(
            self.model._meta.app_label, self.model._meta.model_name, date.today().strftime('%Y%m%d')))
        self.prepare_dataframe()

    def prepare_dataframe(self):
        # create dataframes for models
        model = EdcModelToDataFrame(self.model, add_columns_for=self.add_columns_for)
        consent = EdcModelToDataFrame(self.consent_model)

        # merge
        self.df = pd.merge(model.dataframe, consent.dataframe[
            ['subject_identifier', 'consent_datetime', 'dob', 'recruitment_clinic',
             'citizen', 'gender', 'study_site', 'version']],
            on='subject_identifier', how='left', suffixes=['', '_consent'])

        self.columns = sorted(list(self.df.columns))
        # unused export columns
        export_columns = ['export_change_type', 'export_uuid', 'exported', 'exported_datetime']
        for column in export_columns:
            self.columns.pop(self.columns.index(column))
        # push consent and other columns to the front
        consent_columns = ['subject_identifier', 'report_datetime', 'gender', 'dob',
                           'citizen', 'study_site', 'consent_datetime', 'version']
        for column in consent_columns:
            self.columns.pop(self.columns.index(column))
        self.columns = consent_columns + self.columns
        # push audit columns to the end
        audit_columns = ['registered_subject_id', 'id', 'created', 'modified', 'user_created', 'user_modified',
                         'hostname_created', 'hostname_modified', 'revision']
        for column in audit_columns:
            self.columns.pop(self.columns.index(column))
        self.columns = self.columns + audit_columns

    def to_csv(self):
        self.df[self.columns].to_csv(self.csv_filename, index=False)
