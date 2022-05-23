from django.contrib import admin
from .models import Contract,Order,User,Work,UserHouse


# Register your models here.

admin.site.register(Contract)
admin.site.register(Order)
admin.site.register(User)
admin.site.register(Work)
admin.site.register(UserHouse)