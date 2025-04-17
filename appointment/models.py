from django.db import models
from user.models import Doctor, Patient
from medication.models import Medication
from django.utils import timezone

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')
    date = models.DateField(null=True)  # 预约日期
    hour = models.IntegerField(null=True)  # 预约小时
    reason = models.TextField(null=True)
    medication = models.ForeignKey(Medication, on_delete=models.SET_NULL, null=True)  # 药物关联
    dose = models.IntegerField(null=True)  # 剂量
    status_choices = [
        ('pending', '待处理'),
        ('completed', '已完成'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)  # 病人预约时间，自动记录创建时的时间
    updated_at = models.DateTimeField(auto_now=True)  # 医生处理时间，自动记录每次更新的时间


class AppointmentBalance(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_balances')
    date = models.DateField()  # 预约日期
    hour = models.IntegerField()  # 预约小时
    remaining_quota = models.IntegerField(default=10)  # 剩余名额，默认为每小时的总名额

    class Meta:
        unique_together = ('doctor', 'date', 'hour')  # 确保每个医生每小时每天只有一个余额记录
