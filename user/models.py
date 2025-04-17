from django.db import models

class Doctor(models.Model):
    GENDER_CHOICES = [
        ("m", "Male"),
        ("f", "Female")
    ]

    doctor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Full Name")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='m', verbose_name="Gender")
    age = models.IntegerField(verbose_name="Age")
    department = models.CharField(max_length=50, verbose_name="Department")
    title = models.CharField(max_length=50, verbose_name="Title")
    info = models.CharField(max_length=255, verbose_name="Biography", help_text="No more than 250 characters.")
    contact_number = models.CharField(max_length=20, verbose_name="Phone Number / Username")
    password = models.CharField(max_length=30, verbose_name="Password")

    def __str__(self):
        return f"{self.name} (ID: {self.doctor_id})"


class Patient(models.Model):
    GENDER_CHOICES = [
        ("m", "Male"),
        ("f", "Female")
    ]

    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Full Name")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='m', verbose_name="Gender")
    age = models.IntegerField(verbose_name="Age")
    address = models.CharField(max_length=255, verbose_name="Home Address")
    info = models.CharField(max_length=255, verbose_name="Medical Info", help_text="No more than 250 characters.")
    contact_number = models.CharField(max_length=20, verbose_name="Phone Number / Username")
    password = models.CharField(max_length=30, verbose_name="Password")

    def __str__(self):
        return f"{self.name} (ID: {self.patient_id})"


class Nurse(models.Model):
    GENDER_CHOICES = [
        ("m", "Male"),
        ("f", "Female")
    ]

    nurse_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Full Name")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='m', verbose_name="Gender")
    age = models.IntegerField(verbose_name="Age")
    department = models.CharField(max_length=50, verbose_name="Department")
    title = models.CharField(max_length=50, verbose_name="Title")
    info = models.CharField(max_length=255, verbose_name="Biography", help_text="No more than 250 characters.")
    contact_number = models.CharField(max_length=20, verbose_name="Phone Number / Username")
    password = models.CharField(max_length=30, verbose_name="Password")

    def __str__(self):
        return f"{self.name} (ID: {self.nurse_id})"
