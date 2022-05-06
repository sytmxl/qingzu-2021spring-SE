from django.shortcuts import render
import json
from django.http import JsonResponse

# Create your views here.

'''
注册：
输入：账号密码手机号邮箱
成功跳转：个人信息完善
失败返回
'''
def register(request):
    return JsonResponse()

'''
完善个人资料：
输入：个人详细信息
成功跳转：主界面
失败给出提示
'''

def infofill(request):
    return JsonResponse()

'''
登录：（管理员和用户一起登录）
输入：账号密码
跳转：主界面或管理员界面
'''

def login(request):
    return JsonResponse()




