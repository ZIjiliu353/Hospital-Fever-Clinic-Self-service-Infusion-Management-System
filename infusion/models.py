from django.db import models
from appointment.models import Appointment
from user.models import  Nurse


class InfusionSeat(models.Model):
    seat_number = models.IntegerField(primary_key=True)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number}"


class Infusion(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    seat = models.ForeignKey(InfusionSeat, on_delete=models.CASCADE, null=True)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, null=True)  # 护士外键
    check_in_status = models.BooleanField(default=False)  # 报到状态
    sit_down_status = models.BooleanField(default=False)  # 坐下状态

    # 输液状态选项
    INFUSION_STATUS_CHOICES = [
        ('not_started', '未开始'),
        ('infusing', '输液中'),
        ('waiting_for_removal', '待拔针'),
        ('completed', '输液完成'),
        ('cancelled', '已取消'),
    ]
    infusion_status = models.CharField(max_length=20, choices=INFUSION_STATUS_CHOICES, default='not_started')

    def __str__(self):
        return f'Infusion - {self.id}'