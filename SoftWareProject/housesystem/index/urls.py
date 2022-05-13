from django.urls import path
from .views import *

urlpatterns = [
    path('',index),
    path('<int:house_id>/houseinfo',houseinfo),
    path('<int:house_id>/housetrade',housetrade),
]