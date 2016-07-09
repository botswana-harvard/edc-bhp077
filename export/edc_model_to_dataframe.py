import pandas as pd
import numpy as np


class EdcModelToDataFrame(object):
    """
        e = EdcModelToDataFrame(ClinicVlResult, add_columns_for='clinic_visit')
        my_df = e.dataframe
    """

    def __init__(self, model=None, queryset=None, query_filter=None, add_columns_for=None):
        query_filter = query_filter or {}
        qs = queryset or model.objects.all()
        self.model = model or qs.model
        columns = self.columns(qs, add_columns_for)
        qs = qs.values_list(*columns.keys()).filter(**query_filter)
        self.dataframe = pd.DataFrame(list(qs), columns=columns.keys())
        self.dataframe.rename(columns=columns, inplace=True)
        self.dataframe.fillna(value=np.nan, inplace=True)
        for column in list(self.dataframe.select_dtypes(include=['datetime64[ns, UTC]']).columns):
            self.dataframe[column] = self.dataframe[column].astype('datetime64[ns]')

    def columns(self, qs, add_columns_for):
        """ """
        columns = qs[0].__dict__.keys()
        columns = self.remove_sys_columns(columns)
        columns = dict(zip(columns, columns))
        if add_columns_for in columns or '{}_id'.format(add_columns_for) in columns:
            if add_columns_for.endswith('_visit'):
                columns.update({
                    '{}__appointment__visit_definition__code'.format(add_columns_for):
                    'visit_code'})
                columns.update({
                    '{}__appointment__registered_subject__subject_identifier'.format(add_columns_for):
                    'subject_identifier'})
                try:
                    del columns['subject_identifier']
                except KeyError:
                    pass
            elif add_columns_for == 'registered_subject':
                columns.update({'registered_subject__subject_identifier': 'subject_identifier'})
        return columns

    def remove_sys_columns(self, columns):
        names = ['_state', '_user_container_instance', 'using']
        for name in names:
            try:
                columns.remove(name)
            except ValueError:
                pass
        return columns

