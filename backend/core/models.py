from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime

class EquipmentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True)
    summary_data = models.JSONField()
    class Meta:
        ordering = ['-upload_date'] 