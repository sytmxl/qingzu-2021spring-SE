from django.db import models
# Create your models here.


class Info(models.Model):
    InfoID = models.IntegerField(primary_key=True,null=False)
    Datetime = models.DateTimeField(null=False)
    UserID = models.IntegerField(null=False) #没设置外键
    WorkID = models.IntegerField(null=True)  #没设置外键
    Content = models.CharField(max_length=255,null=False)

class Picture(models.Model):
    PicID = models.IntegerField(primary_key=True,null=False)
    # PicPath = models.CharField(max_length=255,null=False) 由于前端的需要，这部分交给前端存储，后端不再设置文件路径
    HouseID = models.IntegerField(null=True)  #没设置外键
    WorkID = models.IntegerField(null=True)   #没设置外键

class House(models.Model):
    HouseID = models.IntegerField(primary_key=True,null=False)
    Address = models.CharField(max_length=255,null=False)
    Type = models.CharField(max_length=255,null=False)
    DateRequirement = models.CharField(max_length=1,null=True)
    Rent = models.IntegerField(null=False)
    Landlord = models.CharField(max_length=255,null=True)
