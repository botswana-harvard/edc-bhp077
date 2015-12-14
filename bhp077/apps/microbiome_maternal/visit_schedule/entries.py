from edc.subject.visit_schedule.classes.visit_schedule_configuration import RequisitionPanelTuple, EntryTuple
from edc_constants.constants import NOT_REQUIRED, REQUIRED, ADDITIONAL, NOT_ADDITIONAL


maternal_history_entries = (
    EntryTuple(10L, u'microbiome_maternal', u'maternallocator', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(20L, u'microbiome_maternal', u'maternaldemographics', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(40L, u'microbiome_maternal', u'maternalmedicalhistory', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(50L, u'microbiome_maternal', u'maternalobstericalhistory', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(60L, u'microbiome_maternal', u'maternalclinicalhistory', NOT_REQUIRED, NOT_ADDITIONAL),
    EntryTuple(70L, u'microbiome_maternal', u'maternalarvhistory', NOT_REQUIRED, ADDITIONAL),
    EntryTuple(80L, u'microbiome_maternal', u'maternalarvpreg', NOT_REQUIRED, ADDITIONAL),
    EntryTuple(200L, u'microbiome_maternal', u'maternaldeathreport', NOT_REQUIRED, ADDITIONAL),
    EntryTuple(210L, u'microbiome_maternal', u'maternaloffstudy', NOT_REQUIRED, ADDITIONAL))

maternal_delivery_entries = (
    EntryTuple(10L, u'microbiome_maternal', u'maternallabourdel', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(20L, u'microbiome_maternal', u'maternallabdelmed', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(30L, u'microbiome_maternal', u'maternallabdelclinic', NOT_REQUIRED, ADDITIONAL),
    EntryTuple(40L, u'microbiome_maternal', u'maternallabdeldx', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(45L, u'microbiome_maternal', u'maternalheightweight', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(48L, u'microbiome_maternal', u'maternalbreasthealth', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(50L, u'microbiome_maternal', u'maternalarvpreg', NOT_REQUIRED, ADDITIONAL),
    EntryTuple(70L, u'microbiome_maternal', u'maternalbreasthealth', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(80L, u'microbiome_maternal', u'maternalpostfumed', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(200L, u'microbiome_maternal', u'maternaldeathreport', NOT_REQUIRED, ADDITIONAL),
    EntryTuple(210L, u'microbiome_maternal', u'maternaloffstudy', NOT_REQUIRED, ADDITIONAL))

maternal_monthly_entries = (
    EntryTuple(10L, u'microbiome_maternal', u'maternalpostfu', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(20L, u'microbiome_maternal', u'maternalpostfudx', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(25L, u'microbiome_maternal', u'maternalpostfumed', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(30L, u'microbiome_maternal', u'sexualreproductivehealth', NOT_REQUIRED, ADDITIONAL),
    EntryTuple(40L, u'microbiome_maternal', u'maternalsrh', NOT_REQUIRED, ADDITIONAL),
    EntryTuple(50L, u'microbiome_maternal', u'maternalarvpost', NOT_REQUIRED, ADDITIONAL),
    EntryTuple(60L, u'microbiome_maternal', u'maternalarvpostadh', NOT_REQUIRED, ADDITIONAL),
    EntryTuple(70L, u'microbiome_maternal', u'maternalbreasthealth', REQUIRED, NOT_ADDITIONAL),
    EntryTuple(90L, u'microbiome_maternal', u'rapidtestresult', NOT_REQUIRED, ADDITIONAL),
    EntryTuple(200L, u'microbiome_maternal', u'maternaldeathreport', NOT_REQUIRED, ADDITIONAL),
    EntryTuple(210L, u'microbiome_maternal', u'maternaloffstudy', NOT_REQUIRED, ADDITIONAL))

maternal_requisition_entries = (
    RequisitionPanelTuple(
        10L, u'microbiome_lab', u'maternalrequisition',
        'Viral Load', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        20L, u'microbiome_lab', u'maternalrequisition',
        'Breast Milk (Storage)', 'STORAGE', 'BM', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        30L, u'microbiome_lab', u'maternalrequisition',
        'Vaginal swab (Storage)', 'STORAGE', 'VS', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        40L, u'microbiome_lab', u'maternalrequisition',
        'Rectal swab (Storage)', 'STORAGE', 'RS', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        50L, u'microbiome_lab', u'maternalrequisition',
        'Skin Swab (Storage)', 'STORAGE', 'SW', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        60L, u'microbiome_lab', u'maternalrequisition',
        'Vaginal Swab (multiplex PCR)', 'TEST', 'VS', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        70L, u'microbiome_lab', u'maternalrequisition',
        'Hematology (ARV)', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        80L, u'microbiome_lab', u'maternalrequisition',
        'CD4 (ARV)', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
)
