from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField, IntegerField, TextField

# Create your models here.

class EmpPersonal(models.Model):
    name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=60)
    age = models.IntegerField()
    address = models.TextField()
    country = models.CharField(max_length=20)
    otp = models.CharField(max_length=6,default="000000")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   # document = models.FileField(upload_to='media',default="")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'personal_info'
