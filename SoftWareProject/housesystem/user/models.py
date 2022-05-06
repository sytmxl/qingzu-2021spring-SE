from django.db import models
'''
1.建库时少用外键
2.尽可能少更改这一文件，提早确定这个文件的需求
'''
# Create your models here.
#


    # 会员类
class members(models.Model):
    id = models.AutoField(primary_key=True)#写了防报错，不一定要保留


    #管理员（客服）类
class manager(models.Model):
    id = models.AutoField(primary_key=True)  # 写了防报错，不一定要保留
