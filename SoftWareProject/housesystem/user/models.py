from django.db import models
from index.models import House
'''
1.建库时少用外键
2.尽可能少更改这一文件，提早确定这个文件的需求
'''
# Create your models here.
#

class Contract(models.Model):
    ContractID = models.IntegerField(primary_key=True,null=False)
    OrderID = models.IntegerField(null=False)
    FilePath = models.CharField(max_length=50,null=False)

class Order(models.Model):
    OrderID = models.IntegerField(primary_key=True,null=False)
    OrderDate = models.DateTimeField(null=False)
    DueDate = models.DateTimeField(null=False)
    Price = models.IntegerField(null=False)
    Mark = models.IntegerField(null=False)
    Comment = models.CharField(max_length=50,null=False)
    Pay = models.BooleanField(null=False)
    UserID = models.IntegerField(null=False)
    HouseID = models.IntegerField(null=False)

class User(models.Model):
    UserID = models.AutoField(primary_key=True,null=False)
    Email = models.CharField(max_length=255,null=False)
    Username = models.CharField(max_length=255,null=False)
    Password = models.CharField(max_length=255,null=False)
    PicID = models.CharField(max_length=255,null=True)
    ID = models.CharField(max_length=18,null=True)
    Phone = models.CharField(max_length=11,null=True)
    Status = models.CharField(max_length=1,null=True)

class Work(models.Model):
    WorkID = models.IntegerField(primary_key=True,null=False)
    Datatime = models.DateTimeField(null=False)
    HouseID = models.IntegerField(null=False)
    Description = models.CharField(max_length=255,null=False)
    UserID = models.IntegerField(null=False)
    WorkerID = models.IntegerField(null=False)
    Comment = models.CharField(max_length=255,null=True)
    Mark = models.IntegerField(null=True)

class UserHouse(models.Model):
    UserID = models.ForeignKey(User,on_delete=models.CASCADE)
    HouseID = models.ForeignKey(House,on_delete=models.CASCADE)
