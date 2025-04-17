from django.db import models

class Doctor(models.Model):
    genders = [
        ("m", "男"),
        ("f", "女")
    ]

    doctor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="医生姓名")
    gender = models.CharField(max_length=10, choices=genders, default='m', verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄")
    department = models.CharField(max_length=50, verbose_name="科室")
    title = models.CharField(max_length=50, verbose_name="职称")
    info = models.CharField(max_length=255, verbose_name="医生介绍", help_text="不要超过250字")
    contact_number = models.CharField(max_length=20, verbose_name="联系电话/账号")  # 合并为一个字段
    password = models.CharField(max_length=30, verbose_name="密码")

    def __str__(self):
        return f"{self.name} (ID: {self.doctor_id})"

class Patient(models.Model):
    genders = [
        ("m", "男"),
        ("f", "女")
    ]

    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="患者姓名")
    gender = models.CharField(max_length=10, choices=genders, default='m', verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄")
    address = models.CharField(max_length=255, verbose_name="家庭地址")
    info = models.CharField(max_length=255, verbose_name="病人介绍", help_text="不要超过250字")
    contact_number = models.CharField(max_length=20, verbose_name="联系电话/账号")  # 合并为一个字段
    password = models.CharField(max_length=30, verbose_name="密码")

    def __str__(self):
        return f"{self.name} (ID: {self.patient_id})"

class Nurse(models.Model):
    genders = [
        ("m", "男"),
        ("f", "女")
    ]

    nurse_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="护士姓名")
    gender = models.CharField(max_length=10, choices=genders, default='m', verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄")
    department = models.CharField(max_length=50, verbose_name="科室")
    title = models.CharField(max_length=50, verbose_name="职称")
    info = models.CharField(max_length=255, verbose_name="护士介绍", help_text="不要超过250字")
    contact_number = models.CharField(max_length=20, verbose_name="联系电话/账号")  # 合并为一个字段
    password = models.CharField(max_length=30, verbose_name="密码")

    def __str__(self):
        return f"{self.name} (ID: {self.nurse_id})"
