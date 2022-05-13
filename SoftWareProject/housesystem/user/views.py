from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

'''
注册：
输入：账号密码手机号邮箱
成功跳转：个人信息完善
失败返回
'''
@csrf_exempt
def register(request):
    return JsonResponse()

'''
完善个人资料：
输入：个人详细信息
成功跳转：主界面
失败给出提示
'''
@csrf_exempt
def infoFill(request):
    return JsonResponse()

'''
登录：（管理员和用户一起登录）
输入：账号密码
跳转：主界面或管理员界面
'''
@csrf_exempt
def login(request):
    return JsonResponse()


@csrf_exempt
def personalCenter(request):
    return JsonResponse()

@csrf_exempt
def changeInfo(request):
    return JsonResponse()

@csrf_exempt
def refindCode(request):
    return JsonResponse()

@csrf_exempt
def changeCode(request):
    return JsonResponse()

@csrf_exempt
def cancelUser(request):
    return JsonResponse()

@csrf_exempt
def manageOrder(request):
    return JsonResponse()

@csrf_exempt
def repairComplaints(request):
    return JsonResponse()

@csrf_exempt
def repairComplaints(request):
    return JsonResponse()

@csrf_exempt
def collect(request):
    return JsonResponse()

@csrf_exempt
def managerCenter(request):
    return JsonResponse()

@csrf_exempt
def manageUser(request):
    return JsonResponse()

@csrf_exempt
def manageOrder(request):
    return JsonResponse()

@csrf_exempt
def manageOrder(request):
    return JsonResponse()

@csrf_exempt
def dealRepair(request):
    return JsonResponse()

@csrf_exempt
def manageRoom(request):
    return JsonResponse()