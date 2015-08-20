from ...models import Patient
import factory

from datetime import datetime

from edc_constants.choices import GENDER


class PatientFactory(factory.DjangoModelFactory):
    class Meta:
        model = Patient

    patient_identifier = factory.Sequence(lambda n: '066-21444678-{0}'.format(n))
    protocol = 'LIS'
    registration_datetime = datetime.today()
    gender = GENDER[0]
    dob = datetime(1990, 8, 13)
    identity = factory.Sequence(lambda n: '31791851{0}'.format(n))
