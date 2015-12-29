from edc_lab.lab_requisition.classes import site_requisitions
from .models import MaternalRequisition, InfantRequisition

from microbiome.apps.mb.constants import INFANT, MATERNAL

site_requisitions.register(MATERNAL, MaternalRequisition)
site_requisitions.register(INFANT, InfantRequisition)
