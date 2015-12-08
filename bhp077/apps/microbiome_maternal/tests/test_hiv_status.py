from edc_constants.choices import POS_NEG_UNTESTED_REFUSAL, YES_NO_NA, POS_NEG, YES_NO, NO
from edc_constants.constants import NO, YES, POS, NEG, NOT_APPLICABLE, UNKNOWN
from edc_utils.review_derived_variables import ReviewDerivedVariables

from bhp077.apps.microbiome_maternal.models.antenatal_enrollment import AntenatalEnrollment
from bhp077.apps.microbiome_maternal.models.maternal_visit import MaternalVisit


class DerivedHivStatusAnteNatal(ReviewDerivedVariables):

    fields = [
        'current_hiv_status', 'evidence_hiv_status', 'week32_result', 'rapid_test_result',
        'week32_test', 'rapid_test_done', 'valid_regimen', 'valid_regimen_duration']
    models = [AntenatalEnrollment]
    visit_model = MaternalVisit

    opts_current_hiv_status = [tpl[0] for tpl in POS_NEG_UNTESTED_REFUSAL]
    opts_evidence_hiv_status = [tpl[0] for tpl in YES_NO_NA]
    opts_rapid_test_result = [tpl[0] for tpl in POS_NEG] + [None]
    opts_week32_result = [tpl[0] for tpl in POS_NEG] + [None]
    opts_week32_test = [tpl[0] for tpl in YES_NO]
    opts_rapid_test_done = [tpl[0] for tpl in YES_NO_NA]
    opts_valid_regimen = [tpl[0] for tpl in YES_NO_NA]
    opts_valid_regimen_duration = [tpl[0] for tpl in YES_NO_NA]

    def fn_hiv_pos(self, record, *args):
        if record.current_hiv_status == POS and record.evidence_hiv_status == YES:
            return POS
        elif record.current_hiv_status == NEG and record.evidence_hiv_status == YES:
            return NEG
        return None

    def fn_hiv_neg(self, record, *args):
        if record.current_hiv_status == NEG and record.evidence_hiv_status == YES:
            return NEG
        return None

    def fn_hiv_unknown(self, record, *args):
        if record.current_hiv_status == UNKNOWN and record.evidence_hiv_status == NOT_APPLICABLE:
            return UNKNOWN
        return None

    def fn_hiv_eligibility(self, record, *args):
        eligible = False
        if (record.week32_result in [POS, NEG] and
                record.evidence_hiv_status == YES):
            eligible = True
        elif (record.rapid_test_done == YES and record.evidence_hiv_status in [NO, NOT_APPLICABLE] and
                not record.week32_result):
            eligible = True
        elif (record.current_hiv_status == POS and record.evidence_hiv_status == YES and
                record.valid_regimen == YES and record.valid_regimen_duration == YES):
            eligible = True
        elif (record.current_hiv_status == NEG and record.evidence_hiv_status == YES and
              record.valid_regimen != YES and record.valid_regimen_duration != YES):
            eligible = True
        elif record.evidence_hiv_status == NO and record.rapid_test_result != POS:
            eligible = True
        if eligible:
            print(record.week32_test,
                  record.current_hiv_status,
                  record.evidence_hiv_status,
                  record.week32_result,
                  record.rapid_test_done,
                  record.rapid_test_result)
        return eligible
