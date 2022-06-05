from django.db import models
# Create your models here.


class Info(models.Model):
    InfoID = models.AutoField(primary_key=True,null=False)
    Datetime = models.DateTimeField(null=False)
    UserID = models.IntegerField(null=False) #没设置外键
    WorkID = models.IntegerField(null=True)  #没设置外键
    Content = models.CharField(max_length=255,null=False)

class Picture(models.Model):
    PicID = models.AutoField(primary_key=True,null=False)
    PicPath = models.CharField(max_length=255,null=True)
    HouseID = models.IntegerField(null=True)  #没设置外键
    WorkID = models.IntegerField(null=True)   #没设置外键

class House(models.Model):
    HouseID = models.AutoField(primary_key=True,null=False)
    Housename = models.CharField(max_length=255,null=True)
    Housetype = models.CharField(max_length=255,null=True) #户型，例如三室一厅
    Area = models.FloatField(null=True) # 面积
    Floor = models.IntegerField(null=True) # 楼层
    Address = models.CharField(max_length=255,null=True)
    Type = models.CharField(max_length=255,null=True) # 类型，如毛坯
    Rent = models.IntegerField(null=True)
    LandlordName = models.CharField(max_length=255,null=True)
    LandlordPhone = models.CharField(max_length=255, null=True)
    Mark = models.FloatField(null=True,default=0)
    City = models.CharField(max_length=255,null=True)
    Introduction = models.TextField(null=True, default="一、房源优势： 1、此房格局方正，南北向使用率很赞 2、挑高客厅，宽敞大气，精装修，提包入住 二、户型介绍 1、客厅挑高、宽敞舒适、阳光充足 2、卧室搭配的很新颖，使用率很高 3、厨房让您和家人有足够的空间展现私家厨艺 4、连接厨房之间是您和家人享受美味的餐厅，足足可摆下多人桌，让您热情的招待亲朋好友。 三、社区介绍： 1、社区环境好，环境优美，适宜居住，人文素质高，物业管理完善； 2、小区的容及率非常小，属于低密度社区 ，非常适宜居住 3、小区的高，让您感受花园一样的家。 四、交通介绍：地理位置优越，私家车和公共交通都能方便出行。地铁6号线在周围环绕。 五、个人介绍：本房源是全新的房源，发布及时，欢迎来电并实地看房")
    Status = models.BooleanField(null=False,default=False) #标志房屋是否被出租

class Message(models.Model):
    MessageID = models.AutoField(primary_key=True,null=False)
    WorkID = models.IntegerField(null=True)   #没设置外键
    Errornumber = models.IntegerField(null=True)
    UserID = models.IntegerField(null=False) #没设置外键
    Text = models.TextField(null=True)
    Username = models.CharField(max_length=255,null=False)