from bhp077.apps.microbiome_maternal.models import AntenatalEnrollment, PostnatalEnrollment


class EnrollmentStatusHelper(object):

    def __init__(self, registered_subject):
        self.registered_subject = registered_subject

    @property
    def antinatal_enrollment(self):
        try:
            return AntenatalEnrollment.objects.get(registered_subject=self.registered_subject)
        except AntenatalEnrollment.DoesNotExist:
            return False

    @property
    def postnatal_enrollment(self):
        try:
            return PostnatalEnrollment.objects.get(registered_subject=self.registered_subject)
        except AntenatalEnrollment.DoesNotExist:
            return False

    @property
    def is_antinatal_elibigible(self):
        if self.antinatal_enrollment:
            return self.antinatal_enrollment.eligible_for_postnatal
        return False

    @property
    def is_postnatal_elibigible(self):
        if self.antinatal_enrollment:
            return self.antinatal_enrollment.eligible_for_postnatal
        return False

    @property
    def antinatal_postnatal_elibigible(self):
        if self.postnatal_enrollment and self.antinatal_enrollment:
            postnatal = self.postnatal_enrollment
            postnatal.will_breastfeed = self.antinatal_enrollment.will_breastfeed
            postnatal.will_remain_onstudy = self.antinatal_enrollment.will_remain_onstudy
            postnatal.verbal_hiv_status = self.antinatal_enrollment.verbal_hiv_status
            postnatal.evidence_hiv_status = self.antinatal_enrollment.verbal_hiv_status
            return postnatal.postnatal_eligible
        return False

    @property
    def postnatal_elibigible(self):
        if not self.antinatal_enrollment:
            if self.postnatal_enrollment:
                return self.postnatal_enrollment.postnatal_eligible
        return False

    @property
    def is_eligible(self):
        if self.antinatal_postnatal_elibigible:
            return True
        elif self.postnatal_elibigible:
            return True
        elif self.is_antinatal_elibigible:
            return True
        return False
