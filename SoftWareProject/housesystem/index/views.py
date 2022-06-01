from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import re,json
from .models import *
from user.models import *
import datetime
from django.core import serializers

@csrf_exempt
def FirstPage(request): #主界面
    if request.method == 'POST':  # 判断请求方式是否为 POST（要求POST方式）

        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '0':  # 我的订单
            orderlist = []
            order = Order.objects.filter(UserID=user_id,Pay=False)
            #如果用户没有订单?
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate':x.OrderDate.date(),
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
                print(x.DueDate)
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
            print(houselist)
            return JsonResponse({'houselist': houselist})
        elif function_id == '3':  # 个人资料
            return JsonResponse({'introduction': user.Introduction})
        elif function_id == '4': # 主页
            '''
            user_id是前端传来的用户id，根据这个id在数据库中获取用户可能喜欢的房源，返回值是房源ID+房源图片ID+房源图片路径（对应数据库中的HouseID，PicID和PicPath）列表的json格式。
            用户收藏的房源存储在user下的UserHouse类中。如有必要的话可以添加一个新的类，里面存储用户浏览的房源，根据此来做推荐算法。
            '''

            return JsonResponse()
        elif function_id == '5': #查看
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            return JsonResponse({'Mark':house.Mark,
                                 'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'Introduction': house.Introduction})
        elif function_id == '6': # 收藏
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            if UserHouse.objects.filter(UserID=user_id,HouseID=house_id).exists() == True:
                return JsonResponse({'errornumber': 3, 'message': "用户已收藏！"})
            else:
                new_collection = UserHouse(UserID=user_id,HouseID=house_id,Mark=house.Mark)
                new_collection.save()
                return JsonResponse({'errornumber': 1, 'message': "成功登录并收藏！"})#未成功登录的情况暂时由前端处理
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def search(request): #我要租房
    if request.method == 'POST':  # 判断请求方式是否为 POST（要求POST方式）
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
        elif function_id == '4': # 主页

            return JsonResponse()
        elif function_id == '5': #查看
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            return JsonResponse({'Mark':house.Mark,
                                 'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'Introduction': house.Introduction})
        elif function_id == '6': # 收藏
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            if UserHouse.objects.filter(UserID=user_id,HouseID=house_id).exists() == True:
                return JsonResponse({'errornumber': 3, 'message': "用户已收藏！"})
            else:
                new_collection = UserHouse(UserID=user_id,HouseID=house_id,Mark=house.Mark)
                new_collection.save()
                return JsonResponse({'errornumber': 1, 'message': "成功登录并收藏！"})#未成功登录的情况暂时由前端处理
        elif function_id == '7': #房源搜索
            house_name = querylist.get('house_name')
            houses = House.objects.filter(Housename__contains=house_name)
            # return JsonResponse(list(response), safe=False, json_dumps_params={'ensure_ascii': False})
            houselist = []
            for house in houses:
                pics = Picture.objects.filter(HouseID=house.HouseID).values('PicPath')
                houselist.append({
                    'HouseID': house.HouseID,
                    'Housename': house.Housename,
                    'Floor': house.Floor,
                    'Rent': house.Rent,
                    'Type': house.Type,
                    'Area': house.Area,
                    'PicPathList': list(pics)
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '8': #房源筛选
            houses = House.objects.filter(# 具体get名称未对接
                City=querylist.get('city'),
                Type=querylist.get('type')
            )

            rent = querylist.get('rent')
            if rent == 0:
                houses.filter(rent__lte=1000)
            if rent == 1:
                houses.filter(rent__gte=1000).filter(rent__lte=3000)
            if rent == 2:
                houses.filter(rent__gte=3000).filter(rent__lte=5000)
            if rent == 3:
                houses.filter(rent__gte=5000).filter(rent__lte=10000)
            if rent == 4:
                houses.filter(rent__gte=10000)

            return JsonResponse(list(houses))
        elif function_id == '9': #提交申请
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            start_day = datetime.datetime.strptime(querylist.get('start_day'), '%Y-%m-%d').date()
            finish_day = datetime.datetime.strptime(querylist.get('finish_day'), '%Y-%m-%d').date()
            day = (finish_day-start_day).days
            type = querylist.get('type')
            price = house.Rent*day
            if type == '1': #短租
                return JsonResponse({'DayRent':house.Rent,'day':day,'Price':price})
            elif type == '2':
                return JsonResponse({'LandlordName':house.LandlordName,'Username':user.Username,'Address':house.Address,'Area':house.Area,'day':day,'starttime':str(start_day)})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def order(request):
    if request.method == 'POST':  # 判断请求方式是否为 POST（要求POST方式）
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
        elif function_id == '4': # 主页

            return JsonResponse()
        elif function_id == '5': #正在处理
            order = Order.objects.filter(UserID=user_id,Pay=False)
            orderlist = []
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
        elif function_id == '6': #历史记录
            order = Order.objects.filter(UserID=user_id,Pay=True)
            orderlist = []
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
        elif function_id == '7': #订单详情
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            order = Order.objects.get(HouseID=house_id,Pay=True)
            return JsonResponse({'Mark':house.Mark,
                                 'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'OrderDate': order.OrderDate.date(),
                                 'DueDate': order.DueDate.date(),
                                 'Introduction': house.Introduction})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def info_order(request):
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
    else:
        return  JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def service(request):
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
        elif function_id == '5': # 历史订单
            order = Order.objects.filter(UserID=user_id, Pay=True)
            orderlist = []
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
        elif function_id == '6': #正在处理保修
            work = Work.objects.filter(UserID=user_id,Status=False)
            worklist = []
            for x in work:
                y=House.objects.get(HouseID=x.HouseID)
                worklist.append({
                    'Datetime':x.Datetime,
                    'WorkID':x.WorkID,
                    'Address':y.Address
                })
            return JsonResponse({'worklist': worklist})
        elif function_id == '7': #历史完成报修
            work = Work.objects.filter(UserID=user_id,Status=True)
            worklist = []
            for x in work:
                y=House.objects.get(HouseID=x.HouseID)
                worklist.append({
                    'Datetime':x.Datetime,
                    'WorkID':x.WorkID,
                    'Address':y.Address
                })
            return JsonResponse({'worklist': worklist})
        elif function_id == '8': # 查看历史订单详情
            order_id = querylist.get('order_id')
            order = Order.objects.get(OrderID=order_id)
            house_id = order.HouseID
            house = House.objects.get(HouseID=house_id)
            return JsonResponse({'Mark':house.Mark,
                                 'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'OrderDate': order.OrderDate.date(),
                                 'DueDate': order.DueDate.date(),
                                 'Introduction': house.Introduction})
        elif function_id == '9': #我要报修投诉
            order_id = querylist.get('order_id')
            order = Order.objects.get(OrderID=order_id)
            house_id = order.HouseID
            house = House.objects.get(HouseID=house_id)
            return JsonResponse({'Mark':house.Mark,
                                 'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'OrderDate': order.OrderDate.date(),
                                 'DueDate': order.DueDate.date(),
                                 'Introduction': house.Introduction})
        elif function_id == '10':#查看投诉详情
            work_id=querylist.get('work_id')
            work = Work.objects.get(WorkID=work_id)
            house_id = work.HouseID
            house = House.objects.get(HouseID=house_id)
            order = Order.objects.get(HouseID=house_id)
            picture = Picture.objects.get(WorkID=work_id)
            return JsonResponse({'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'OrderDate': order.OrderDate.date(),
                                 'DueDate': order.DueDate.date(),
                                 'Introduction': house.Introduction,
                                 'ComplainPic':picture.PicPath,
                                 'ComplainText':work.Description})
        elif function_id == '11':#联系师傅/客服
            work_id = querylist.get('work_id')
            list = Message.objects.filter(WorkID=work_id)
            messagelist = []
            for x in list:
                messagelist.append({
                    'errnum':x.Errornumber,
                    'id':x.UserID,
                    'text':x.Text,
                    'name':x.Username
                })
            return JsonResponse({'massagelist':messagelist})
        elif function_id == '12':#进入我要报修/投诉界面
            order_id = querylist.get('order_id')
            order = Order.objects.get(OrderID=order_id)
            house_id = order.HouseID
            house = House.objects.get(HouseID=house_id)
            return JsonResponse({'Mark':house.Mark,
                                 'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'OrderDate': order.OrderDate.date(),
                                 'DueDate': order.DueDate.date(),
                                 'Introduction': house.Introduction})
        elif function_id == '13': #提交
            now = datetime.datetime.now().date()
            order_id = querylist.get('order_id')
            order = Order.objects.get(OrderID=order_id)
            house_id = order.HouseID
            description = querylist.get('description')
            picpath = querylist.get('picpath')
            new_work = Work(Datetime=now, HouseID=house_id, Description=description, UserID=user_id,Phone=user.Phone,Username=user.Username)
            new_work.save()
            work = Work.objects.get(Datetime=now, HouseID=house_id, Description=description, UserID=user_id)
            new_picture = Picture(PicPath=picpath, HouseID=house_id, WorkID=work.WorkID)
            new_picture.save()
            return JsonResponse({'errornumber': 1, 'message': "提交投诉/报修成功！"})
        elif function_id == '14': #提交留言
            work_id = querylist.get('work_id')
            Errornumber = querylist.get('errornumber')
            UserID = querylist.get('id')
            Text = querylist.get('text')
            Username = querylist.get('name')
            new_message = Message(Errornumber=Errornumber,UserID = UserID,Text = Text,Username = Username)
            new_message.save()
            return JsonResponse({'errornumber': 1, 'message': "留言成功！"})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def info_complain(request):
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
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def connect(request):
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


    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def collection(request):
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
        elif function_id == '5': #查看
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            return JsonResponse({'Mark':house.Mark,
                                 'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'Introduction': house.Introduction})
        elif function_id == '6':  #删除
            house_id = querylist.get('house_id')
            userhouse = UserHouse.objects.get(HouseID=house_id,UserID=user_id)
            userhouse.delete()
            houselist = []
            for x in UserHouse.objects.filter(UserID=user_id):
                houselist.append({
                    'HouseID': x.HouseID
                })
            return JsonResponse({'houselist': houselist})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def information(request):
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
        elif function_id == '5': #短租
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            house.Status = True
            house.save()
            start_day = datetime.datetime.strptime(querylist.get('start_day'), '%Y-%m-%d').date()
            finish_day = datetime.datetime.strptime(querylist.get('finish_day'), '%Y-%m-%d').date()
            day = (finish_day-start_day).days
            price = house.Rent*day
            new_order = Order(OrderDate = start_day , DueDate = finish_day , Price=price , Pay=True , UserID=user_id , HouseID=house_id)
            new_order.save()
            return JsonResponse({'errornumber': 0, 'message': "短租成功！"})
        elif function_id == '6': #长租
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            house.Status = True
            house.save()
            start_day = datetime.datetime.strptime(querylist.get('start_day'), '%Y-%m-%d').date()
            finish_day = datetime.datetime.strptime(querylist.get('finish_day'), '%Y-%m-%d').date()
            day = (finish_day-start_day).days
            price = house.Rent*day
            new_order = Order(OrderDate = start_day,DueDate = finish_day,Price=price,Pay=False,UserID=user_id,HouseID=house_id)
            new_order.save()
            filepath = querylist.get('filepath')
            order_id = Order.objects.get(HouseID=house_id).OrderID
            new_contract = Contract(OrderID=order_id,FilePath=filepath)
            new_contract.save()
            return JsonResponse({'errornumber': 1, 'message': "长租成功！"})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

