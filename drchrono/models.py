from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime
import pytz


# Create your models here.

@python_2_unicode_compatible
class PatientModel(models.Model):
    # doctor_id = models.ForeignKey(DoctorModel, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    doctor_id = models.IntegerField(null=False)
    gender = models.CharField(max_length=10)
    birthday = models.DateField(default=datetime.date)
    patient_id = models.IntegerField(null=False, primary_key=True)
    patient_email = models.EmailField(default="")

    def __str__(self):
        separator = "|"
        patient = (str(self.patient_id), self.first_name, self.last_name, str(self.birthday), str(self.patient_email))
        return separator.join(patient)


class AppointmentModel(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    doctor = models.IntegerField()
    patient = models.IntegerField()
    office = models.IntegerField()
    exam_room = models.IntegerField()
    reason = models.CharField(max_length=1000, blank=True)
    status = models.CharField(max_length=20)
    deleted_flag = models.BooleanField()
    scheduled_time = models.DateTimeField()
    # some extra fields for arrival and called in time information
    arrival_time = models.DateTimeField(blank=True)
    call_in_time = models.DateTimeField(blank=True)

    def __str__(self):
        separator = "|"
        appt = ('pid:' + str(self.patient), 'did:' + str(self.doctor), 'status:' + str(self.status), 'apt:' + str(self.scheduled_time) )
        return separator.join(appt)
