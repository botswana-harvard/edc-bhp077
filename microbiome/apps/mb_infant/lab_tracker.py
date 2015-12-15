from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.lab_tracker.classes import HivLabTracker


class InfantHivLabTracker(HivLabTracker):
    subject_type = 'infant'
    trackers = []

site_lab_tracker.register(InfantHivLabTracker)
