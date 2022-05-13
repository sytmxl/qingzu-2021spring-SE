from django.db import models

# Create your models here.

class house(models.Model):
    id = models.AutoField(primary_key=True)#写了防报错，不一定要保留