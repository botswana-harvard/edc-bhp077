from edc.base.form.forms import BaseModelForm
from ..models import PostnatalEnrollment, AntenatalEnrollment

from edc.subject.registration.models import RegisteredSubject


class PostnatalEnrollmentForm(BaseModelForm):

    def __init__(self, *args, **kwargs):
        if not kwargs.get('instance', None):
            ante_natal_enrollment = self.is_ante_natal_available(
                self.registered_subject(kwargs.get('initial').get('registered_subject'))
            )
            if ante_natal_enrollment:
                initial = kwargs.get('initial')
                initial.update(citizen=ante_natal_enrollment.citizen,
                        is_diabetic=ante_natal_enrollment.is_diabetic,
                        on_tb_treatment=ante_natal_enrollment.on_tb_treatment,
                        breastfeed_for_a_year=ante_natal_enrollment.breastfeed_for_a_year,
                        instudy_for_a_year=ante_natal_enrollment.instudy_for_a_year,
                        verbal_hiv_status=ante_natal_enrollment.verbal_hiv_status,
                        evidence_hiv_status=ante_natal_enrollment.evidence_hiv_status,
                        valid_regimen=ante_natal_enrollment.valid_regimen,
                        process_rapid_test=ante_natal_enrollment.process_rapid_test,
                        date_of_rapid_test=ante_natal_enrollment.date_of_rapid_test,
                        rapid_test_result=ante_natal_enrollment.rapid_test_result
                )
                kwargs.update(initial=initial)
        super(PostnatalEnrollmentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PostnatalEnrollment
        fields = '__all__'

    def is_ante_natal_available(self, registered_subject):
        try:
            return AntenatalEnrollment.objects.get(registered_subject=registered_subject)
        except AntenatalEnrollment.DoesNotExist:
            return False

    def registered_subject(self, id):
        try:
            return RegisteredSubject.objects.get(id=id)
        except RegisteredSubject.DoesNotExist:
            pass
