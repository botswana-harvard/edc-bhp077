from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.lab_tracker.classes import HivLabTracker

from microbiome.apps.mb.constants import INFANT


class InfantHivLabTracker(HivLabTracker):
    subject_type = INFANT
    trackers = []

site_lab_tracker.register(InfantHivLabTracker)
