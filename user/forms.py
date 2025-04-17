from django import forms
from user.models import Doctor, Patient,Nurse


class DoctorLoginForm(forms.Form):
    doctor_contact_number = forms.CharField(max_length=20, label="医生账号/联系电话")
    doctor_password = forms.CharField(widget=forms.PasswordInput, label="密码")

class PatientLoginForm(forms.Form):
    patient_contact_number = forms.CharField(max_length=20, label="病人账号/联系电话")
    patient_password = forms.CharField(widget=forms.PasswordInput, label="密码")

class NurseLoginForm(forms.Form):
    nurse_contact_number = forms.CharField(max_length=20, label="护士账号/联系电话")
    nurse_password = forms.CharField(widget=forms.PasswordInput, label="密码")

class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class NurseRegistrationForm(forms.ModelForm):
    class Meta:
        model = Nurse
        fields = '__all__'
