# user/backends.py

from django.contrib.auth.backends import ModelBackend
from .models import Doctor
from .models import Patient
from .models import Nurse


class DoctorBackend(ModelBackend):
    def authenticate(self, request, contact_number=None, password=None, **kwargs):
        try:
            doctor = Doctor.objects.get(contact_number=contact_number)
        except Doctor.DoesNotExist:
            return None

        if doctor.password == password:
            return doctor

        return None

class PatientBackend(ModelBackend):
    def authenticate(self, request, contact_number=None, password=None, **kwargs):
        try:
            patient = Patient.objects.get(contact_number=contact_number)
        except Patient.DoesNotExist:
            return None

        if patient.password == password:
            return patient

        return None

class NurseBackend(ModelBackend):
    def authenticate(self, request, contact_number=None, password=None, **kwargs):
        try:
            nurse = Nurse.objects.get(contact_number=contact_number)
        except Nurse.DoesNotExist:
            return None

        if nurse.password == password:
            return nurse

        return None
