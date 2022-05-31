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
    PicPath = models.CharField(max_length=255,null=True)
    HouseID = models.IntegerField(null=True)  #没设置外键
    WorkID = models.IntegerField(null=True)   #没设置外键

class House(models.Model):
    HouseID = models.IntegerField(primary_key=True,null=False)
    Housename = models.CharField(max_length=255,null=True)
    Housetype = models.CharField(max_length=255,null=True) #户型，例如三室一厅
    Area = models.CharField(max_length=255,null=True) # 面积
    Floor = models.CharField(max_length=255,null=True) # 楼层
    Address = models.CharField(max_length=255,null=True)
    Type = models.CharField(max_length=255,null=True) # 类型，如毛坯
    Rent = models.IntegerField(null=True)
    LandlordName = models.CharField(max_length=255,null=True)
    LandlordPhone = models.CharField(max_length=255, null=True)
    Mark = models.IntegerField(null=True,default=0)
    City = models.CharField(max_length=255,null=True)
    Introduction = models.TextField(null=True)
    Status = models.BooleanField(null=False,default=False) #标志房屋是否被出租