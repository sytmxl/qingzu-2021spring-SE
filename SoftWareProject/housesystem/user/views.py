from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
from .models import *
from index.models import *

@csrf_exempt
def Register(request):
    if request.method == 'POST':  # 判断请求方式是否为 POST（要求POST方式）
        querylist = request.POST
        username = querylist.get('username')  # 获取请求数据
        password_1 = querylist.get('password_1')
        password_2 = querylist.get('password_2')
        #phone = querylist.get('phone')
        email = querylist.get('email')
        if(re.match("^[A-Za-z0-9]+$",username)==None): # 任意长度的字符和数字组合
            return JsonResponse({'errornumber': 2, 'message': "用户名格式错误:只能输入字母和数字的组合"})
        elif(User.objects.filter(Username=username).exists() or User.objects.filter(Email=email).exists()):
            return JsonResponse({'errornumber': 3, 'message': "用户名或邮箱已存在"})
        elif(re.match("^[A-Za-z0-9]+$",password_1)==None): # 任意长度的字符和数字组合
            return JsonResponse({'errornumber': 4, 'message': "密码格式错误：只能输入字母和数字的组合"})
        elif(password_1 != password_2):
            return JsonResponse({'errornumber': 5, 'message': "两次输入的密码不一致"})
        #elif(re.match("^\d{11}$",phone)==None):   # 任意长度的字符和数字组合
        #    return JsonResponse({'errornumber': 6, 'message': "手机号格式错误"})
        elif(re.match("^([a-zA-Z\d][\w-]{2,})@(\w{2,})\.([a-z]{2,})(\.[a-z]{2,})?$",email)==None): #// 非下划线的单词字符 + 2个以上单词字符 + @ + 2位以上单词字符域名 + .2位以上小写字母做域名后缀 + (.2位以上二重域名后缀)
            return JsonResponse({'errornumber': 7, 'message': "邮箱格式错误"})
        else:
            new_user = User(Username=username,Password=password_1,Email=email,Status='Y') # Y代表用户，G代表管理员，S代表师傅
            new_user.save()
            return JsonResponse({'errornumber': 0, 'message': "注册成功",'user_id':new_user.UserID})
    else:
        return JsonResponse({'errornumber': 1, 'message': "请求方式错误"})

@csrf_exempt
def Login(request):
    if request.method == 'POST':  # 判断请求方式是否为 POST（要求POST方式）
        querylist = request.POST
        password = querylist.get('password')
        # loginway = querylist.get('login') #前端传来登陆方式
        email = querylist.get('email')
        if User.objects.filter(Email=email).exists() == True:
            loginuser = User.objects.get(Email=email)
        else:
            return JsonResponse({'errornumber': 3, 'message': "用户不存在，请注册"})
            #注册保证用户名和邮箱唯一
        if(loginuser.Password!=password):
            return JsonResponse({'errornumber': 4, 'message': "密码错误，请重试"})
        elif(loginuser.Password==password):
            if(loginuser.Status=='Y'):
                return JsonResponse({'errornumber': 0, 'message': "欢迎用户",'User_id':loginuser.UserID,'Username':loginuser.Username})
            elif(loginuser.Status=='G'):
                return JsonResponse({'errornumber': 1, 'message': "欢迎管理员",'User_id':loginuser.UserID,'Username':loginuser.Username})
            elif(loginuser.Status=='S'):
                return JsonResponse({'errornumber': 2, 'message': "欢迎师傅",'User_id':loginuser.UserID,'Username':loginuser.Username})
    else:
        return JsonResponse({'error': 5, 'message': "请求方式错误"})

@csrf_exempt
def user(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '0':  # 我的订单
            orderlist = []
            order = Order.objects.filter(UserID=user_id,Pay=False)
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '1':  # 保修投诉
            orderlist = []
            order = Order.objects.filter(UserID=user_id)
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '2':  # 我的收藏
            houselist = []
            for x in UserHouse.objects.filter(UserID=user_id):
                houselist.append({
                    'HouseID': x.HouseID
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '3':  # 个人资料
            return JsonResponse({'introduction': user.Introduction})
        elif function_id == '4':  # 主页

            return JsonResponse()
        elif function_id == '5': #详细资料
            return JsonResponse({'PicID':user.PicID,'Username':user.Username,'Phone':user.Phone,'City':user.City,'Job':user.Job})
        elif function_id == '6': #修改个人资料
            user = User.objects.get(UserID=user_id)
            user.Introduction = querylist.get('introduction')
            user.save()
            return JsonResponse({'introduction': user.Introduction})
        elif function_id == '7': #修改个人资料
            user = User.objects.get(UserID=user_id)
            user.PicID = querylist.get('PicID')
            user.Username = querylist.get('Username')
            user.Phone = querylist.get('Phone')
            user.City = querylist.get('City')
            user.Job = querylist.get('Job')
            user.save()
            return JsonResponse({'PicID': user.PicID, 'Username': user.Username, 'Phone': user.Phone, 'City': user.City,'Job': user.Job})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def RepairMan_SelfInfo(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '4': #修改头像（这里可能要修改）
            new_picture = Picture(PicPath = querylist.get('PicPath'))
            new_picture.save()
            return JsonResponse({'errornumber': 0, 'message': "头像更改成功"})
        elif function_id == '5': #修改电话
            phone = querylist.get('phone')
            if (re.match("^\d{11}$", phone) == None):  # 任意长度的字符和数字组合
                return JsonResponse({'errornumber': 3, 'message': "手机号格式错误"})
            else:
                return JsonResponse({'errornumber': 0, 'message': "手机号更改成功"})
        elif function_id == '6': #修改密码
            original_password = querylist.get('original_password')
            new_password1 = querylist.get('new_password1')
            new_password2 = querylist.get('new_password2')
            if(original_password != user.Password):
                return JsonResponse({'errornumber': 4, 'message': "密码错误"})
            elif(new_password1 != new_password2):
                return JsonResponse({'errornumber': 5, 'message': "两次输入的密码不一致"})
            elif(re.match("^[A-Za-z0-9]+$",new_password1)==None):
                return JsonResponse({'errornumber': 6, 'message': "密码格式错误，只能输入数字和字母的组合"})
            else:
                user.Password=new_password1
                user.save()
                return JsonResponse({'errornumber': 0, 'message': "用户密码更改成功"})
        else:
            return worker_index(request)
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def History_Work(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '4':#查看详细信息
            list = Work.objects.filter(WorkerID=user_id,Status = True)
            worklist = []
            for x in list:
                y = User.objects.get(UserID=x.UserID)
                z = House.objects.get(HouseID=x.HouseID)
                worklist.append({
                    'Datetime':x.Datetime,
                    'WorkID':x.WorkID,
                    'HouseID':x.HouseID,
                    'UserID':x.UserID,
                    'Username':y.Username,
                    'Phone':y.Phone,
                    'Address':z.Address
                })
            work_id = querylist.get('work_id')
            work = Work.objects.get(WorkID=work_id)
            renter = User.objects.get(UserID=work.UserID)
            house = House.objects.get(HouseID=work.HouseID)
            detailwork = []
            detailwork.append({
                'Datetime':work.Datetime,
                'WorkID':work.WorkID,
                'HouseID':work.HouseID,
                'UserID':work.UserID,
                'Username':renter.Username,
                'Phone':renter.Phone,
                'Address':house.Address,
                'Description':work.Description,
                'Comment':work.Comment
            })
            piclist = Picture.objects.filter(WorkID=work_id)
            picturelist = []
            for x in piclist:
                picturelist.append(x.PicPath)
            return JsonResponse({'detailwork':detailwork,'worklist':worklist,'picturelist':picturelist})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def Todo_Work(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '4': #联系师傅/客服
            work_id = querylist.get('work_id')
            list = Message.objects.filter(WorkID=work_id)
            messagelist = []
            for x in list:
                messagelist.append({
                    'errnum': x.Errornumber,
                    'id': x.UserID,
                    'text': x.Text,
                    'name': x.Username
                })
            return JsonResponse({'massagelist': messagelist})
        elif function_id == '5': #提交留言
            work_id = querylist.get('work_id')
            Errornumber = querylist.get('errornumber')
            UserID = querylist.get('id')
            Text = querylist.get('text')
            Username = querylist.get('name')
            new_message = Message(Errornumber=Errornumber, UserID=UserID, Text=Text, Username=Username,WorkID=work_id)
            new_message.save()
            return JsonResponse({'errornumber': 1, 'message': "留言成功！"})
        elif function_id == '6': #查看报修/投诉详情
            work_id = querylist.get('work_id')
            work = Work.objects.get(WorkID=work_id)
            house_id = work.HouseID
            house = House.objects.get(HouseID=house_id)
            order = Order.objects.get(HouseID=house_id)
            picture = Picture.objects.get(WorkID=work_id)
            return JsonResponse({'HouseID': house.HouseID,
                                 'Housename': house.Housename,
                                 'Rent': house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'OrderDate': order.OrderDate.date(),
                                 'DueDate': order.DueDate.date(),
                                 'Introduction': house.Introduction,
                                 'ComplainPic': picture.PicPath,
                                 'ComplainText': work.Description})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def worker_index(request):
    querylist = request.POST
    function_id = querylist.get('function_id')
    user_id = querylist.get('user_id')
    user = User.objects.get(UserID=user_id)
    if function_id == '1': #我的资料
        picture = Picture.objects.get(PicID=user.PicID)
        return JsonResponse({'PicPath':picture.PicPath,'Username':user.Username,'UserID':user.UserID,'Phone':user.Phone,'City':user.City})
    elif function_id == '2': #历史工单
        list = Work.objects.filter(WorkerID=user_id,Status = True)
        worklist = []
        for x in list:
            y=User.objects.get(UserID=x.UserID)
            z=House.objects.get(HouseID=x.HouseID)
            worklist.append({
                'Datetime':x.Datetime,
                'WorkID':x.WorkID,
                'HouseID':x.HouseID,
                'UserID':x.UserID,
                'Username':y.Username,
                'Phone':y.Phone,
                'Address':z.Address
            })
        return JsonResponse({'worklist':worklist})
    elif function_id == '3': #正在处理工单
        list = Work.objects.filter(WorkerID=user_id,Status = False)
        worklist = []
        for x in list:
            y=User.objects.get(UserID=x.UserID)
            z=House.objects.get(HouseID=x.HouseID)
            worklist.append({
                'Datetime':x.Datetime,
                'WorkID':x.WorkID,
                'HouseID':x.HouseID,
                'UserID':x.UserID,
                'Username':y.Username,
                'Phone':y.Phone,
                'Address':z.Address
            })
        return JsonResponse({'worklist':worklist})

