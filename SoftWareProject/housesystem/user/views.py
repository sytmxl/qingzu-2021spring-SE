from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
from .models import *

@csrf_exempt
def Register(request):
    if request.method == 'POST':  # 判断请求方式是否为 POST（要求POST方式）
        querylist = request.POST
        username = querylist.get('username')  # 获取请求数据
        password_1 = querylist.get('password_1')
        password_2 = querylist.get('password_2')
        phone = querylist.get('phone')
        email = querylist.get('email')
        if(re.match("^[A-Za-z0-9]+$",username)==None): # 任意长度的字符和数字组合
            return JsonResponse({'errornumber': 2, 'message': "用户名格式错误:只能输入字母和数字的组合"})
        elif(User.objects.filter(Username=username).exists() or User.objects.filter(Email=email).exists()):
            return JsonResponse({'errornumber': 3, 'message': "用户名或邮箱已存在"})
        elif(re.match("^[A-Za-z0-9]+$",password_1)==None): # 任意长度的字符和数字组合
            return JsonResponse({'errornumber': 4, 'message': "密码格式错误：只能输入字母和数字的组合"})
        elif(password_1 != password_2):
            return JsonResponse({'errornumber': 5, 'message': "两次输入的密码不一致"})
        elif(re.match("^\d{11}$",phone)==None):   # 任意长度的字符和数字组合
            return JsonResponse({'errornumber': 6, 'message': "手机号格式错误"})
        elif(re.match("^([a-zA-Z\d][\w-]{2,})@(\w{2,})\.([a-z]{2,})(\.[a-z]{2,})?$",email)==None): #// 非下划线的单词字符 + 2个以上单词字符 + @ + 2位以上单词字符域名 + .2位以上小写字母做域名后缀 + (.2位以上二重域名后缀)
            return JsonResponse({'errornumber': 7, 'message': "邮箱格式错误"})
        else:
            new_user = User(Username=username,Password=password_1,Phone=phone,Email=email,Status='Y') # Y代表用户，G代表管理员，S代表师傅
            new_user.save()
            return JsonResponse({'errornumber': 0, 'message': "注册成功",'user_id':new_user.UserID})
    else:
        return JsonResponse({'errornumber': 1, 'message': "请求方式错误"})

'''
完善个人资料：
输入：个人详细信息
成功跳转：主界面
失败给出提示
'''
@csrf_exempt
def infoFill(request):
    return JsonResponse()

@csrf_exempt
def Login(request):
    if request.method == 'POST':  # 判断请求方式是否为 POST（要求POST方式）
        querylist = request.POST
        password = querylist.get('password')
        loginway = querylist.get('login') #前端传来登陆方式
        print(loginway)
        print(password)
        if(loginway=='email'):
            email = querylist.get('email')
            if User.objects.filter(Email=email).exists() == True:
                loginuser = User.objects.get(Email=email)
            else:
                return JsonResponse({'errornumber': 3, 'message': "用户不存在，请注册"})
        elif(loginway=='username'):
            username = querylist.get('username')
            if User.objects.filter(Username=username).exists() == True:
                loginuser = User.objects.get(Username=username)
            else:
                return JsonResponse({'errornumber': 3, 'message': "用户不存在，请注册"})
            #注册保证用户名和邮箱唯一
        if(loginuser.Password!=password):
            return JsonResponse({'errornumber': 4, 'message': "密码错误，请重试"})
        elif(loginuser.Password==password):
            if(loginuser.Status=='Y'):
                return JsonResponse({'error': 0, 'message': "欢迎用户"})
            elif(loginuser.Status=='G'):
                return JsonResponse({'error': 1, 'message': "欢迎管理员"})
            elif(loginuser.Status=='S'):
                return JsonResponse({'error': 2, 'message': "欢迎师傅"})
    else:
        return JsonResponse({'error': 5, 'message': "请求方式错误"})


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