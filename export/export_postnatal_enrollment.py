import os
import pandas as pd

from datetime import date
from microbiome.export.edc_model_to_dataframe import EdcModelToDataFrame
from microbiome.apps.mb_maternal.models import MaternalVisit, PostnatalEnrollment, MaternalConsent

csv_filename = os.path.expanduser('~/postnatal_enrollment_{}.csv'.format(date.today().strftime('%Y%m%d')))

# create dataframes for models
enrollment = EdcModelToDataFrame(PostnatalEnrollment, add_columns_for='registered_subject')
consent = EdcModelToDataFrame(MaternalConsent)

# merge
df = pd.merge(enrollment.dataframe, consent.dataframe[
    ['subject_identifier', u'consent_datetime', 'dob', 'recruitment_clinic',
     'citizen', 'gender', 'study_site','version']],
    on='subject_identifier', how='left', suffixes=['', '_consent'])

columns = sorted(list(df.columns))
# unused export columns
export_columns = ['export_change_type', 'export_uuid', 'exported', 'exported_datetime']
for column in export_columns:
    columns.pop(columns.index(column))
# push consent and other columns to the front
consent_columns = ['subject_identifier', 'report_datetime', 'gender', 'dob',
                   'citizen', 'study_site', 'registered_subject_id', 'consent_datetime', 'version']
for column in consent_columns:
    columns.pop(columns.index(column))
columns = consent_columns + columns
# push audit columns to the end
audit_columns = ['id', 'created', 'modified', 'user_created', 'user_modified',
                 'hostname_created', 'hostname_modified', 'revision']
for column in audit_columns:
    columns.pop(columns.index(column))
columns = columns + audit_columns

# export as csv
df[columns].to_csv(csv_filename, index=False)

