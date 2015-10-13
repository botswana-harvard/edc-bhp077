from edc.entry_meta_data.managers import RequisitionMetaDataManager


class RequisitionManager(RequisitionMetaDataManager):

    def get_by_natural_key(self, requisition_identifier):
        return self.get(requisition_identifier=requisition_identifier)
