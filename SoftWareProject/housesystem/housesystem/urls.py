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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
import index.views
import user.views

urlpatterns = [
    path('/api/admin/', admin.site.urls),
    path('/api/FirstPage/', index.views.FirstPage), #主界面网站
    path('/api/search/',index.views.search),
    path('/api/order/',index.views.order),
    path('/api/info_order/',index.views.info_order),
    path('/api/service/',index.views.service),
    path('/api/info_complain/',index.views.info_complain),
    path('/api/connect/',index.views.connect),
    path('/api/collection/',index.views.collection),
    path('/api/information/',index.views.information),
    path('/api/user/',user.views.user),
    path('/api/Login/', user.views.Login), #和用户有关的网址，注册登录个人信息等
    path('/api/Register/',user.views.Register),
    path('/api/RepairMan_SelfInfo/',user.views.RepairMan_SelfInfo),
    path('/api/History_Work/',user.views.History_Work),
    path('/api/Todo_Work/',user.views.Todo_Work),
    path('/api/Commander_FirstPage/',user.views.Commander_FirstPage),
    path('/api/Manage_User/',user.views.Manage_User),
    path('/api/Manage_House/',user.views.Manage_House),
    path('/api/Manage_RM/',user.views.Manage_RM),
    path('/api/Manage_Contract/',user.views.Manage_Contract),
    path('/api/UnManaged_Contract/',user.views.UnManaged_Contract),
    path('/api/Manage_Complain/',user.views.Manage_Complain),
    path('/api/Managed_Complain/',user.views.Managed_Complain),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
