"""housesystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import index.views
import user.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('FirstPage/', index.views.FirstPage), #主界面网站
    path('search/',index.views.search),
    path('order/',index.views.order),
    path('info_order/',index.views.info_order),
    path('service/',index.views.service),
    path('info_complain/',index.views.info_complain),
    path('connect/',index.views.connect),
    path('collection/',index.views.collection),
    path('information/',index.views.information),
    path('user/',user.views.user),
    path('Login/', user.views.Login), #和用户有关的网址，注册登录个人信息等
    path('Register/',user.views.Register),
    path('RepairMan_SelfInfo/',user.views.RepairMan_SelfInfo),
    path('History_Work/',user.views.History_Work),
    path('Todo_Work/',user.views.Todo_Work),
]

