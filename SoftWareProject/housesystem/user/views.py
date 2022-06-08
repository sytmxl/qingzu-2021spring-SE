from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
from .models import *
from index.models import *
from .sendemail import *

@csrf_exempt
def Register(request):
    if request.method == 'POST':  # 判断请求方式是否为 POST（要求POST方式）
        querylist = request.POST
        function_id = querylist.get('function_id')
        if function_id == '1':
            email = querylist.get('email')
            code = sendcode(email)  # 成功发送返回字符串形式6为验证码 否则返回'X'
            if code == 'X':
                return JsonResponse({'errornumber': 8, 'message': "发送邮件失败"})
            return JsonResponse({'errornumber': 0, 'code': code})
        else:
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
                return JsonResponse({'errornumber': 0, 'message': "注册成功",'user_id':new_user.UserID,'username':new_user.Username})
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
                return JsonResponse({'errornumber': 0, 'message': "欢迎用户",'User_id':loginuser.UserID,'Username':loginuser.Username,'avatar_url':loginuser.avatar_url})
            elif(loginuser.Status=='G'):
                return JsonResponse({'errornumber': 1, 'message': "欢迎管理员",'User_id':loginuser.UserID,'Username':loginuser.Username,'avatar_url':loginuser.avatar_url})
            elif(loginuser.Status=='S'):
                return JsonResponse({'errornumber': 2, 'message': "欢迎师傅",'User_id':loginuser.UserID,'Username':loginuser.Username,'avatar_url':loginuser.avatar_url})
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
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': house.HouseID,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                    'Floor': house.Floor,
                    'Housename': house.Housename
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '3':  # 个人资料
            return JsonResponse({'introduction': user.Introduction})
        elif function_id == '4':  # 主页

            return JsonResponse()
        elif function_id == '5': #详细资料
            return JsonResponse({'avatar_url':user.avatar_url,'Username':user.Username,'Phone':user.Phone,'City':user.City,'Job':user.Job})
        elif function_id == '6': #修改个人资料
            user = User.objects.get(UserID=user_id)
            user.Introduction = querylist.get('introduction')
            user.save()
            return JsonResponse({'introduction': user.Introduction})
        elif function_id == '7': #修改个人资料
            user.Username = querylist.get('Username')
            user.Phone = querylist.get('Phone')
            user.City = querylist.get('City')
            user.Job = querylist.get('Job')
            user.save()
            return JsonResponse({'Username': user.Username, 'Phone': user.Phone, 'City': user.City,'Job': user.Job,'avatar':user.avatar.name})
        elif function_id == '8': #修改头像
            avatar = request.FILES.get('avatar')
            suffix = '.' + avatar.name.split('.')[-1]
            avatar.name = str(user_id)+'头像'+suffix
            user.avatar= avatar
            user.save()
            user.avatar_url = "http://127.0.0.1:8000/media/" + user.avatar.name
            user.save()
            return JsonResponse({'avatar_url': user.avatar_url})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def RepairMan_SelfInfo(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '4': #修改头像
            avatar = request.FILES.get('avatar')
            suffix = '.' + avatar.name.split('.')[-1]
            avatar.name = str(user_id)+'头像'+suffix
            user.avatar= avatar
            user.save()
            user.avatar_url = "http://127.0.0.1:8000/media/" + user.avatar.name
            user.save()
            return JsonResponse({'errornumber': 0, 'message': "头像更改成功",'avatar_url':user.avatar_url})
        elif function_id == '5': #修改电话
            phone = querylist.get('phone')
            if (re.match("^\d{11}$", phone) == None):  # 任意长度的字符和数字组合
                return JsonResponse({'errornumber': 3, 'message': "手机号格式错误"})
            else:
                user.Phone=phone
                user.save()
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
        elif function_id == '7': #修改邮箱
            email = querylist.get('email')
            if (re.match("^([a-zA-Z\d][\w-]{2,})@(\w{2,})\.([a-z]{2,})(\.[a-z]{2,})?$",email) == None):  # // 非下划线的单词字符 + 2个以上单词字符 + @ + 2位以上单词字符域名 + .2位以上小写字母做域名后缀 + (.2位以上二重域名后缀)
                return JsonResponse({'errornumber': 7, 'message': "邮箱格式错误"})
            else:
                user.Email = email
                user.save()
                return JsonResponse({'errornumber': 0, 'message': "用户邮箱更改成功"})
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
                'Comment':work.Comment,
                'Mark':work.Mark
            })
            picture = work.Picture_url
            return JsonResponse({'detailwork':detailwork,'worklist':worklist,'picture':picture})
        else:
            return worker_index(request)
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
            picture = work.Picture_url
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
                                 'ComplainPic': picture,
                                 'ComplainText': work.Description})
        else:
            return worker_index(request)
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def worker_index(request):
    querylist = request.POST
    function_id = querylist.get('function_id')
    user_id = querylist.get('user_id')
    user = User.objects.get(UserID=user_id)
    if function_id == '1': #我的资料
        return JsonResponse({'Username':user.Username,'UserID':user.UserID,'Phone':user.Phone,'City':user.City,'Email':user.Email,'avatar_url':user.avatar_url})
    elif function_id == '2': #历史工单
        list = Work.objects.filter(WorkerID=user_id,Status = True)
        worklist = []
        for x in list:
            y = User.objects.get(UserID=x.UserID)
            z = House.objects.get(HouseID=x.HouseID)
            worklist.append({
                'Datetime': x.Datetime,
                'WorkID': x.WorkID,
                'HouseID': x.HouseID,
                'UserID': x.UserID,
                'Username': y.Username,
                'Phone': y.Phone,
                'Address': z.Address,
                'Description': x.Description,
                'Comment': x.Comment
            })
        return JsonResponse({'worklist':worklist})
    elif function_id == '3': #正在处理工单
        list = Work.objects.filter(WorkerID=user_id,Status = False)
        worklist = []
        for x in list:
            y = User.objects.get(UserID=x.UserID)
            z = House.objects.get(HouseID=x.HouseID)
            worklist.append({
                'Datetime': x.Datetime,
                'WorkID': x.WorkID,
                'HouseID': x.HouseID,
                'UserID': x.UserID,
                'Username': y.Username,
                'Phone': y.Phone,
                'Address': z.Address,
                'Description': x.Description,
                'Comment': x.Comment
            })
        return JsonResponse({'worklist':worklist})


@csrf_exempt
def Commander_FirstPage(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        if function_id == '9':  # 修改头像
            user_id = querylist.get('user_id')
            user = User.objects.get(UserID=user_id)
            avatar = request.FILES.get('avatar')
            suffix = '.' + avatar.name.split('.')[-1]
            avatar.name = str(user_id) + '头像' + suffix
            user.avatar = avatar
            user.save()
            user.avatar_url = "http://127.0.0.1:8000/media/" + user.avatar.name
            user.save()
            return JsonResponse({'errornumber': 0, 'message': "头像更改成功", 'avatar_url': user.avatar_url})
        elif function_id == '10': # 修改电话
            user_id = querylist.get('user_id')
            user = User.objects.get(UserID=user_id)
            phone = querylist.get('phone')
            try:
                if (re.match("^\d{11}$", phone) == None):  # 任意长度的字符和数字组合
                    return JsonResponse({'errornumber': 3, 'message': "手机号格式错误"})
            except:
                return JsonResponse({'errornumber': 3, 'message': "手机号格式错误"})
            else:
                user.Phone=phone
                user.save()
                return JsonResponse({'errornumber': 0, 'message': "手机号更改成功"})
        elif function_id == '11':  # 修改密码
            user_id = querylist.get('user_id')
            user = User.objects.get(UserID=user_id)
            original_password = querylist.get('original_password')
            new_password1 = querylist.get('new_password1')
            new_password2 = querylist.get('new_password2')
            if (original_password != user.Password):
                return JsonResponse({'errornumber': 4, 'message': "密码错误"})
            elif (new_password1 != new_password2):
                return JsonResponse({'errornumber': 5, 'message': "两次输入的密码不一致"})
            elif (re.match("^[A-Za-z0-9]+$", new_password1) == None):
                return JsonResponse({'errornumber': 6, 'message': "密码格式错误，只能输入数字和字母的组合"})
            else:
                user.Password = new_password1
                user.save()
                return JsonResponse({'errornumber': 0, 'message': "用户密码更改成功"})
        elif function_id == '12':  # 修改邮箱
            user_id = querylist.get('user_id')
            user = User.objects.get(UserID=user_id)
            email = querylist.get('email')
            if re.match("^([a-zA-Z\d][\w-]{2,})@(\w{2,})\.([a-z]{2,})(\.[a-z]{2,})?$", email) is None:  # // 非下划线的单词字符 + 2个以上单词字符 + @ + 2位以上单词字符域名 + .2位以上小写字母做域名后缀 + (.2位以上二重域名后缀)
                return JsonResponse({'errornumber': 7, 'message': "邮箱格式错误"})
            else:
                user.Email = email
                user.save()
                return JsonResponse({'errornumber': 0, 'message': "邮箱更改成功"})
        else:
            return admin_sidebar(request)
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})


@csrf_exempt
def Manage_User(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        if function_id == '9':  # 修改资料
            user_id = querylist.get('user_id')
            user = User.objects.get(UserID=user_id)
            name = querylist.get('name')
            phone = querylist.get('phone')
            city = querylist.get('city')
            email = querylist.get('email')
            '''order = Order.objects.filter(UserID=user_id).latest()
            house = House.objects.get(HouseID=order.HouseID)
            address = house.Address'''
            if (re.match("^\d{11}$", phone) == None):  # 任意长度的字符和数字组合
                return JsonResponse({'errornumber': 3, 'message': "手机号格式错误"})
            if phone != '':
                user.Phone = phone
            if name != '':
                user.Username = name
            if city != '':
                user.City = city
            if email != '':
                user.Email = email
            user.save()
            return JsonResponse({'errornumber': 0, 'message': "租客信息更改成功"})
        elif function_id == '10':  # 删除
            try:
                user_id = querylist.get('user_id')
                User.objects.get(UserID=user_id).delete()
                return JsonResponse({'errornumber': 0, 'message': "租客删除成功"})
            except:
                return JsonResponse({'errornumber': 1, 'message': "租客删除失败"})
        elif function_id == '11': # 用户名搜索
            user_name = querylist.get('user_name')
            try:
                users = User.objects.filter(Username__contains=user_name, Status='Y')
                userlist = []
                for user in users:
                    userlist.append({'UserID': user.UserID,
                                     'Email': user.Email,
                                     'Phone': user.Phone,
                                     'City': user.City,
                                     'Username': user.Username,
                                     'Introduction': user.Introduction,
                                     'Job': user.Job,
                                     'Password': user.Password,
                                     'Login': user.Login
                                     })
            except:
                return JsonResponse({'errornumber': 1, 'message': "搜索失败，无该用户"})
            return JsonResponse({'userlist': userlist})
        elif function_id == '12':   # id 搜索
            id = querylist.get('id')
            try:
                user = User.objects.get(UserID=id, Status='Y')
                return JsonResponse({
                    'UserID': user.UserID,
                    'Email': user.Email,
                    'Phone': user.Phone,
                    'City': user.City,
                    'Username': user.Username,
                    'Introduction': user.Introduction,
                    'Job': user.Job,
                    'Password': user.Password,
                    'Login': user.Login
                    })
            except:
                return JsonResponse({'errornumber': 1, 'message': "搜索失败，无该用户"})
        else:
            return admin_sidebar(request)
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})


@csrf_exempt
def Manage_House(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        if function_id == '9': # 查看图片
            house_id = querylist.get('house_id')
            pics = Picture.objects.filter(HouseID=house_id)
            piclist = []
            for pic in pics:
                piclist.append({
                    'PicID': pic.PicID,
                    'Path': pic.PicPath
                })
            return JsonResponse({'piclist': piclist})
        elif function_id == '10': #房源搜索
            house_name = querylist.get('house_name')
            houses = House.objects.filter(Housename__contains=house_name)
            # return JsonResponse(list(response), safe=False, json_dumps_params={'ensure_ascii': False})
            houselist = []
            for house in houses:
                pics = Picture.objects.filter(HouseID=house.HouseID).values('PicPath')
                houselist.append({
                    'HouseID': house.HouseID,
                    'Housename': house.Housename,
                    'Landlordname': house.LandlordName,
                    'Address': house.Address,
                    'Phone': house.LandlordPhone,
                    'Floor': house.Floor,
                    'Rent': house.Rent,
                    'Type': house.Type,
                    'Housetype': house.Housetype,
                    'Area': house.Area,
                    'PicPathList': list(pics)
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '13':   # id search
            id = querylist.get('id')
            try:
                house = House.objects.get(HouseID=id)
                pics = Picture.objects.filter(HouseID=house.HouseID).values('PicPath')
                return JsonResponse({
                    'HouseID': house.HouseID,
                    'Housename': house.Housename,
                    'Landlordname': house.LandlordName,
                    'Address': house.Address,
                    'Phone': house.LandlordPhone,
                    'Floor': house.Floor,
                    'Rent': house.Rent,
                    'Type': house.Type,
                    'Housetype': house.Housetype,
                    'Area': house.Area,
                    'PicPathList': list(pics)
                })
            except:
                return JsonResponse({'errornumber': 1, 'message': "搜索失败，无该房源"})
        elif function_id == '11':  # 下架房源(删除）
            try:
                house_id = querylist.get('house_id')
                pics = Picture.objects.filter(HouseID=house_id)
                for pic in pics:
                    pic.Pic.delete()
                    pic.delete()
                House.objects.get(HouseID=house_id).delete()
                return JsonResponse({'errornumber': 0, 'message': "下架成功"})
            except:
                return JsonResponse({'errornumber': 1, 'message': "下架失败"})
        elif function_id == '12':  # 新增房源
            try:
                id = querylist.get('house_id')
                house = House(
                    HouseID=querylist.get('house_id'),
                    Housename=querylist.get('house_name'),
                    LandlordPhone=querylist.get('phone'),
                    LandlordName=querylist.get('landlord_name'),
                    Address=querylist.get('address'),
                    Type=querylist.get('type'),
                    Rent=querylist.get('rent'),
                    City=querylist.get('city'),
                    Housetype=querylist.get('house_type'),
                    Area=querylist.get('area'),
                    Floor=querylist.get('floor'),
                )
                house.save()
                piclist = [request.FILES.get('pic1'), request.FILES.get('pic2'), request.FILES.get('pic3'),
                           request.FILES.get('pic4'), request.FILES.get('pic5')]
                i = 1
                for pic in piclist:
                    try:
                        print(pic.name)
                    except:
                        continue
                    suffix = '.' + pic.name.split('.')[-1]
                    pic.name = "房源" + str(id) + "图片" + str(i) + suffix
                    url = "http://127.0.0.1:8000/media/" + pic.name
                    pic = Picture(PicPath=url, HouseID=id, Pic=pic)
                    pic.save()
                    i += 1
                return JsonResponse({'errornumber': 0, 'message': "添加成功"})
            except:
                return JsonResponse({'errornumber': 1, 'message': "添加失败"})
        elif function_id == '14':  # 新增房源图片
            try:
                id = querylist.get('house_id')
                piclist = [request.FILES.get('pic1'), request.FILES.get('pic2'), request.FILES.get('pic3'),
                           request.FILES.get('pic4'), request.FILES.get('pic5')]
                i = 1
                for pic in piclist:
                    try:
                        print(pic.name)
                    except:
                        continue
                    suffix = '.' + pic.name.split('.')[-1]
                    pic.name = "房源" + str(id) + "图片" + str(i) + suffix
                    url = "http://127.0.0.1:8000/media/" + pic.name
                    pic = Picture(PicPath=url, HouseID=id, Pic=pic)
                    pic.save()
                    i += 1
                return JsonResponse({'errornumber': 0, 'message': "添加成功"})
            except:
                return JsonResponse({'errornumber': 1, 'message': "添加失败"})
        else:
            return admin_sidebar(request)
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})


@csrf_exempt
def Manage_RM(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        if function_id == '9':  # 师傅搜索
            worker_name = querylist.get('worker_name')
            workers = User.objects.filter(Username__contains=worker_name, Status='S')
            workerlist = []
            for worker in workers:
                workerlist.append({
                    'workerID': worker.UserID,
                    'workername': worker.Username,
                    'phone': worker.Phone,
                    'place': worker.City,
                    'email': worker.Email
                })
            return JsonResponse({'workerlist': workerlist})
        elif function_id == '12':   # id search
            id = querylist.get('id')
            try:
                worker = User.objects.get(UserID=id, Status='S')
                return JsonResponse({
                    'workerID': worker.UserID,
                    'workername': worker.Username,
                    'phone': worker.Phone,
                    'place': worker.City,
                    'email': worker.Email
                })
            except:
                return JsonResponse({'errornumber': 1, 'message': "搜索失败，无该师傅"})
        elif function_id == '10':  # 删除师傅
            try:
                worker_id = querylist.get('worker_id')
                User.objects.get(UserID=worker_id).delete()
                return JsonResponse({'errornumber': 0, 'message': "删除成功"})
            except:
                return JsonResponse({'errornumber': 1, 'message': "删除失败"})
        elif function_id == '11':  # 添加师傅
            try:
                id = querylist.get('worker_id')
                worker = User(
                    UserID=querylist.get('id'),
                    Username=querylist.get('name'),
                    Email=querylist.get('email'),
                    Status='S',
                    Phone=querylist.get('phone'),
                    Password=querylist.get('password'),
                    City=querylist.get('city')
                )
                worker.save()
                return JsonResponse({'errornumber': 0, 'message': "添加成功"})
            except:
                return JsonResponse({'errornumber': 1, 'message': "添加失败"})
        else:
            return admin_sidebar(request)
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})


@csrf_exempt
def Manage_Contract(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        if function_id == '9':  # 搜索合同 基于用户名
            name = querylist.get('name')
            users = User.objects.filter(Username__contains=name)
            contracts = []
            for user in users:
                orders = Order.objects.filter(UserID=user.UserID)
                for order in orders:
                    contract = Contract.objects.get(OrderID=order.OrderID)
                    if contract.Passed:
                        contracts.append(contract)
            contract_list = []
            for contract in contracts:
                order = Order.objects.get(OrderID=contract.OrderID)
                user = User.objects.get(UserID=order.UserID)
                house = House.objects.get(HouseID=order.HouseID)
                contract_list.append({
                    'contract_id': contract.ContractID,
                    'order_id': order.OrderID,
                    'path': contract.FilePath,
                    'user_id': user.UserID,
                    'house_id': house.HouseID,
                    'user_name': user.Username,
                    'address': house.Address,
                    'rent': house.Rent,
                })
            return JsonResponse({'contract_list': contract_list})
        elif function_id == '12':   # id 搜索
            id = querylist.get('id')
            try:
                contract = Contract.objects.get(ContractID=id)
                if contract.Passed:  # status
                    order = Order.objects.get(OrderID=contract.OrderID)
                    user = User.objects.get(UserID=order.UserID)
                    house = House.objects.get(HouseID=order.HouseID)
                    return JsonResponse({
                        'contract_id': contract.ContractID,
                        'order_id': order.OrderID,
                        'path': contract.FilePath,
                        'user_id': user.UserID,
                        'house_id': house.HouseID,
                        'user_name': user.Username,
                        'address': house.Address,
                        'rent': house.Rent,
                    })
                else:
                    return JsonResponse({'errornumber': 1, 'message': "搜索失败，无该合同"})
            except:
                return JsonResponse({'errornumber': 1, 'message': "搜索失败，无该合同"})
        if function_id == '10': # 查看合同
            contract_id = querylist.get('contract_id')
            contract = Contract.objects.get(ContractID=contract_id)
            path = contract.FilePath
            return JsonResponse({'path': path})
        if function_id == '11': # delete
            try:
                contract_id = querylist.get('contract_id')
                contract = Contract.objects.get(ContractID=contract_id)
                contract.delete()
                order = Order.objects.get(OrderID=contract.OrderID)
                order.delete()
                return JsonResponse({'errornumber': 0, 'message': "删除成功"})
            except:
                return JsonResponse({'errornumber': 1, 'message': "删除失败"})

        else:
            return admin_sidebar(request)
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})


@csrf_exempt
def UnManaged_Contract(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        if function_id == '9':  # 搜索合同 基于用户名
            name = querylist.get('name')
            users = User.objects.filter(Username__contains=name)
            contracts = []
            for user in users:
                orders = Order.objects.filter(UserID=user.UserID)
                for order in orders:
                    print("order: ")
                    print(order.OrderID)
                    contract = Contract.objects.get(OrderID=order.OrderID)
                    print("contract: ")
                    print(contract.ContractID)
                    if not contract.Passed: # status
                        contracts.append(contract)
            contract_list = []
            for contract in contracts:
                order = Order.objects.get(OrderID=contract.OrderID)
                user = User.objects.get(UserID=order.UserID)
                print("order.HouseID:")
                print(order.HouseID)
                house = House.objects.get(HouseID=order.HouseID)
                contract_list.append({
                    'contract_id': contract.ContractID,
                    'order_id': order.OrderID,
                    'path': contract.FilePath,
                    'user_id': user.UserID,
                    'house_id': house.HouseID,
                    'user_name': user.Username,
                    'address': house.Address,
                    'rent': house.Rent,
                })
            return JsonResponse({'contract_list': contract_list})
        elif function_id == '13':   # id 搜索
            id = querylist.get('id')
            try:
                contract = Contract.objects.get(ContractID=id)
                if not contract.Passed:  # status
                    order = Order.objects.get(OrderID=contract.OrderID)
                    user = User.objects.get(UserID=order.UserID)
                    house = House.objects.get(HouseID=order.HouseID)
                    return JsonResponse({
                        'contract_id': contract.ContractID,
                        'order_id': order.OrderID,
                        'path': contract.FilePath,
                        'user_id': user.UserID,
                        'house_id': house.HouseID,
                        'user_name': user.Username,
                        'address': house.Address,
                        'rent': house.Rent,
                    })
                else:
                    return JsonResponse({'errornumber': 1, 'message': "搜索失败，无该合同"})
            except:
                return JsonResponse({'errornumber': 1, 'message': "搜索失败，无该合同"})
        elif function_id == '12':   # 审查合同
            result = querylist.get('result')
            try:

                contract_id = querylist.get('contract_id')
                contract = Contract.objects.get(ContractID=contract_id)
                if result == '1':
                    contract.Result= True
                else:
                    contract.Result = False
                contract.Passed = True
                contract.save()
                return JsonResponse({'errornumber': 0, 'message': "审查成功"})
            except:
                return JsonResponse({'errornumber': 1, 'message': "审查失败"})
        if function_id == '10': # 查看合同
            contract_id = querylist.get('contract_id')
            contract = Contract.objects.get(ContractID=contract_id)
            path = contract.FilePath
            return JsonResponse({'path': path})
        if function_id == '11': # delete
            try:
                contract_id = querylist.get('contract_id')
                contract = Contract.objects.get(ContractID=contract_id)
                contract.delete()
                order = Order.objects.get(OrderID=contract.OrderID)
                order.delete()
                return JsonResponse({'errornumber': 0, 'message': "删除成功"})
            except:
                return JsonResponse({'errornumber': 1, 'message': "删除失败"})
        else:
            return admin_sidebar(request)
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def Manage_Complain(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        if function_id == '9':  # 搜索待处理工单 此时详细信息一并给予
            name = querylist.get('name')
            users = User.objects.filter(Username__contains=name)
            works = []
            for user in users:
                work = Work.objects.filter(UserID=user.UserID)
                for w in work:
                    if w.Status is False:
                        works.append(w)
            worklist = []
            for work in works:
                user = User.objects.get(UserID=work.UserID)
                house = House.objects.get(HouseID=work.HouseID)
                orders = Order.objects.filter(HouseID=house.HouseID)
                for o in orders:
                    order = o
                    break
                worklist.append({
                    'Datetime': work.Datetime,
                    'WorkID': work.WorkID,
                    'HouseID': work.HouseID,
                    'UserID': work.UserID,
                    'WorkerID': work.WorkerID,
                    'Username': user.Username,
                    'Phone': user.Phone,
                    'Address': house.Address,
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
                    'ComplainPic': work.Picture_url,
                    'ComplainText': work.Description
                })
            return JsonResponse({'worklist': worklist})
        elif function_id == '13':   # id search
            id = querylist.get('id')
            try:
                work = Work.objects.get(WorkID=id, Status=False)
                user = User.objects.get(UserID=work.UserID)
                house = House.objects.get(HouseID=work.HouseID)
                order = Order.objects.get(OrderID=work.OrderID)
                return JsonResponse({
                    'Datetime': work.Datetime,
                    'WorkID': work.WorkID,
                    'HouseID': work.HouseID,
                    'UserID': work.UserID,
                    'WorkerID': work.WorkerID,
                    'Username': user.Username,
                    'Phone': user.Phone,
                    'Address': house.Address,
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
                    'ComplainPic': work.Picture_url,
                    'ComplainText': work.Description
                })
            except:
                return JsonResponse({'errornumber': 1, 'message': "搜索失败，无该工单"})
        elif function_id == '10':   # 返回空闲师傅
            workers = User.objects.filter(Status='S', WorkID=0)
            worker_list = []
            for worker in workers:
                worker_list.append({
                    'name': worker.Username,
                    'id': worker.UserID
                })
            return JsonResponse({'worker_list': worker_list})
        elif function_id == '11':   # 分配师傅
            try:
                worker_id_list = querylist.get('worker_id_list')
            except:
                return JsonResponse({'errornumber': 1, 'message': "获取师傅列表错误"})
            try:
                worker_id_list = worker_id_list.split()
            except:
                return JsonResponse({'errornumber': 1, 'message': "分裂错误"})
            try:
                work_id = querylist.get('work_id')
            except:
                return JsonResponse({'errornumber': 1, 'message': "获取工单错误"})
            try:
                print('多个数据')
                for worker_id in worker_id_list:
                    worker = User.objects.get(UserID=int(worker_id))
                    worker.WorkID = work_id
                    worker.save()
            except:
                print('单个数据')
                worker = User.objects.get(UserID=int(worker_id_list))
                worker.WorkID = work_id
                worker.save()
            return JsonResponse({'errornumber': 0, 'message': "分配师傅成功"})
        elif function_id == '12':  # 提交留言
            work_id = querylist.get('work_id')
            UserID = querylist.get('id')
            Text = querylist.get('text')
            Username = querylist.get('name')
            new_message = Message(Errornumber=1, UserID=UserID, Text=Text, Username=Username, WorkID=work_id)
            new_message.save()
            return JsonResponse({'errornumber': 1, 'message': "留言成功！"})
        else:
            return admin_sidebar(request)
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})


@csrf_exempt
def Managed_Complain(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        if function_id == '9':  # 搜索待处理工单 此时详细信息一并给予
            name = querylist.get('name')
            users = User.objects.filter(Username__contains=name)
            works = []
            for user in users:
                work = Work.objects.filter(UserID=user.UserID)
                for w in work:
                    if w.Status is True:
                        works.append(w)
            worklist = []
            for work in works:
                user = User.objects.get(UserID=work.UserID)
                house = House.objects.get(HouseID=work.HouseID)
                orders = Order.objects.filter(HouseID=house.HouseID)
                for o in orders:
                    order = o
                    break
                worklist.append({
                    'Datetime': work.Datetime,
                    'WorkID': work.WorkID,
                    'HouseID': work.HouseID,
                    'UserID': work.UserID,
                    'WorkerID': work.WorkerID,
                    'Username': user.Username,
                    'Phone': user.Phone,
                    'Address': house.Address,
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
                    'ComplainPic': work.Picture_url,
                    'ComplainText': work.Description
                })
            return JsonResponse({'worklist': worklist})
        elif function_id == '10':   # id search
            id = querylist.get('id')
            try:
                work = Work.objects.get(WorkID=id, Status=True)
                user = User.objects.get(UserID=work.UserID)
                house = House.objects.get(HouseID=work.HouseID)
                order = Order.objects.get(OrderID=work.OrderID)
                return JsonResponse({
                    'Datetime': work.Datetime,
                    'WorkID': work.WorkID,
                    'HouseID': work.HouseID,
                    'UserID': work.UserID,
                    'WorkerID': work.WorkerID,
                    'Username': user.Username,
                    'Phone': user.Phone,
                    'Address': house.Address,
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
                    'ComplainPic': work.Picture_url,
                    'ComplainText': work.Description
                })
            except:
                return JsonResponse({'errornumber': 1, 'message': "搜索失败，无该工单"})
        else:
            return admin_sidebar(request)
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})


def admin_sidebar(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        if function_id == '1': # 主页
            id = querylist.get('id')
            try:
                user = User.objects.get(UserID=id)
            except:
                return JsonResponse({'errornumber': 1, 'message': "用户不存在"})
            return JsonResponse({
                'name':user.Username, # 管理员名字
                'id': user.UserID, # 管理员ID
                'phone': user.Phone,
                'email': user.Email,
                'path': user.avatar_url #头像图片路径
            })
        elif function_id == '2':    # 管理租客
            users = User.objects.filter(Status='Y')
            userlist = []
            for user in users:
                userlist.append({'UserID': user.UserID,
                                 'Email': user.Email,
                                 'Phone': user.Phone,
                                 'City': user.City,
                                 'Username': user.Username,
                                 'Introduction': user.Introduction,
                                 'Job': user.Job,
                                 'Password': user.Password,
                                 'Login': user.Login    # 是否登陆
                                 })
            return JsonResponse({'userlist': userlist})
        elif function_id == '3':    # 管理房间
            houses = House.objects.all()
            houselist = []
            for house in houses:
                pics = Picture.objects.filter(HouseID=house.HouseID).values('PicPath')
                houselist.append({
                    'HouseID': house.HouseID,
                    'Housename': house.Housename,
                    'Landlordname': house.LandlordName,
                    'Address': house.Address,
                    'Phone': house.LandlordPhone,
                    'Floor': house.Floor,
                    'Rent': house.Rent,
                    'Type': house.Type,
                    'Housetype': house.Housetype,
                    'Area': house.Area,
                    'PicPathList': list(pics)
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '4':    # 管理师傅
            workers = User.objects.filter(Status='S')
            worker_list = []
            for worker in workers:
                worker_list.append({
                    'name': worker.Username,
                    'id': worker.UserID,
                    'city': worker.City,
                    'phone': worker.Phone,
                    'email': worker.Email
                })
            return JsonResponse({'worker_list': worker_list})
        elif function_id == '5':    # 已处理申诉
            works = Work.objects.filter(Status=True)  # 筛选未处理
            worklist = []
            for work in works:
                user = User.objects.get(UserID=work.UserID)
                house = House.objects.get(HouseID=work.HouseID)
                order = Order.objects.get(OrderID=work.OrderID)
                worklist.append({
                    'Datetime': work.Datetime,
                    'WorkID': work.WorkID,
                    'HouseID': work.HouseID,
                    'UserID': work.UserID,
                    'WorkerID': work.WorkerID,
                    'Username': user.Username,
                    'Phone': user.Phone,
                    'Address': house.Address,
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
                    'ComplainPic': work.Picture_url,
                    'ComplainText': work.Description
                })
            return JsonResponse({'worklist': worklist})
        elif function_id == '6':    # 未处理申诉
            works = Work.objects.filter(Status=False)  # 筛选未处理
            worklist = []
            for work in works:
                user = User.objects.get(UserID=work.UserID)
                house = House.objects.get(HouseID=work.HouseID)
                order = Order.objects.get(OrderID=work.OrderID)
                worklist.append({
                    'Datetime': work.Datetime,
                    'WorkID': work.WorkID,
                    'HouseID': work.HouseID,
                    'UserID': work.UserID,
                    'WorkerID': work.WorkerID,
                    'Username': user.Username,
                    'Phone': user.Phone,
                    'Address': house.Address,
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
                    'ComplainPic': work.Picture_url,
                    'ComplainText': work.Description
                })
            return JsonResponse({'worklist': worklist})
        elif function_id == '7':    # 待处理合同
            contracts = Contract.objects.filter(Passed=False)
            contract_list = []
            for contract in contracts:
                order = Order.objects.get(OrderID=contract.OrderID)
                user = User.objects.get(UserID=order.UserID)
                house = House.objects.get(HouseID=order.HouseID)
                contract_list.append({
                    'contract_id': contract.ContractID,
                    'order_id': order.OrderID,
                    'path': contract.FilePath,
                    'user_id': user.UserID,
                    'house_id': house.HouseID,
                    'user_name': user.Username,
                    'address': house.Address,
                    'rent': house.Rent,
                })
            return JsonResponse({'contract_list': contract_list})
        elif function_id == '8':    # 已处理合同
            contracts = Contract.objects.filter(Passed=True)
            contract_list = []
            for contract in contracts:
                order = Order.objects.get(OrderID=contract.OrderID)
                user = User.objects.get(UserID=order.UserID)
                house = House.objects.get(HouseID=order.HouseID)
                contract_list.append({
                    'contract_id': contract.ContractID,
                    'order_id': order.OrderID,
                    'path': contract.FilePath,
                    'user_id': user.UserID,
                    'house_id': house.HouseID,
                    'user_name': user.Username,
                    'address': house.Address,
                    'rent': house.Rent,
                })
            return JsonResponse({'contract_list': contract_list})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})