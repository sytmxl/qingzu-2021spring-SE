from django.db import models

# Create your models here.

# 会员类
class members(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)