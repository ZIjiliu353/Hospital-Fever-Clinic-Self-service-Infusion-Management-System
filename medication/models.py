from django.db import models

class Medication(models.Model):
    medication_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="药物名")
    expiration_date = models.DateField(verbose_name="保质期到期日")
    current_quantity = models.IntegerField(verbose_name="当前存储量")

    def __str__(self):
        return self.name
