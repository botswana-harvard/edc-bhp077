from edc.lab.lab_requisition.classes import site_requisitions
from .models import MaternalRequisition, InfantRequisition


site_requisitions.register('maternal', MaternalRequisition)
site_requisitions.register('infant', InfantRequisition)
