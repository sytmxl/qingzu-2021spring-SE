from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import re,json
from .models import *
from user.models import *
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
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate': x.OrderDate,
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
                    'OrderDate': x.OrderDate,
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
            用户收藏的房源存储在user下的UserHouse类中。
            '''
            return JsonResponse()
        elif function_id == '5': #查看
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            infolist = []
            infolist.append({'Mark':house.Mark})
            infolist.append({'HouseID':house.HouseID})
            infolist.append({'Housename':house.Housename})
            infolist.append({'Rent':house.Rent})
            infolist.append({'Housetype': house.Housetype})
            infolist.append({'Area': house.Area})
            infolist.append({'Floor': house.Floor})
            infolist.append({'Type': house.Type})
            infolist.append({'Floor': house.Floor})
            infolist.append({'LandlordPhone': house.LandlordPhone})
            infolist.append({'Introduction': house.Introduction})
            # print(infolist)
            return JsonResponse({'infolist':infolist})
        elif function_id == '6': # 收藏，不能重复收藏暂时没有实现
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            new_collection = UserHouse(UserID=user_id,HouseID=house_id,Score=house.Score)
            new_collection.save()
            return JsonResponse({'errornumber': 1, 'message': "成功登录并收藏！"})#未成功登录的情况暂时由前端处理
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def search(request):
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
                    'OrderDate': x.OrderDate,
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
                    'OrderDate': x.OrderDate,
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
            infolist = []
            infolist.append({'Mark':house.Mark})
            infolist.append({'HouseID':house.HouseID})
            infolist.append({'Housename':house.Housename})
            infolist.append({'Rent':house.Rent})
            infolist.append({'Housetype': house.Housetype})
            infolist.append({'Area': house.Area})
            infolist.append({'Floor': house.Floor})
            infolist.append({'Type': house.Type})
            infolist.append({'Floor': house.Floor})
            infolist.append({'LandlordPhone': house.LandlordPhone})
            infolist.append({'Introduction': house.Introduction})
            # print(infolist)
            return JsonResponse({'infolist':infolist})
        elif function_id == '6': # 收藏，不能重复收藏暂时没有实现
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            new_collection = UserHouse(UserID=user_id,HouseID=house_id,Score=house.Score)
            new_collection.save()
            return JsonResponse({'errornumber': 1, 'message': "成功登录并收藏！"})#未成功登录的情况暂时由前端处理
        elif function_id == '7': #房源搜索
            house_name = querylist.get('house_name')
            '''
            house_name是用户传来的待搜索房源名称，返回值是房源ID+房源图片ID+房源图片路径（对应数据库中的HouseID，PicID和PicPath）的json格式。
            '''
            return JsonResponse()
        elif function_id == '8': #房源筛选
            '''
            用户传来的参数可能有很多，见我要租房.png，包括城市，租金等等，返回值是房源ID+房源图片ID+房源图片路径（对应数据库中的HouseID，PicID和PicPath）列表的json格式。
            '''
            return JsonResponse()
        elif function_id == '7':
            return JsonResponse()
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def Order(request):
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
                    'OrderDate': x.OrderDate,
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
                    'OrderDate': x.OrderDate,
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
            order = Order.objects.filter(UserID=user_id,pay=False)
            orderlist = []
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate': x.OrderDate,
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '6': #历史记录
            order = Order.objects.filter(UserID=user_id, pay=True)
            orderlist = []
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate': x.OrderDate,
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '7': #订单详情
            order_id = querylist.get('order_id')
            order = Order.objects.get(OrderID=order_id)
            house_id = order.HouseID
            house = House.objects.get(HouseID=house_id)
            infolist = []
            infolist.append({'Mark':order.Mark}) #订单的评分而非房源的评分
            infolist.append({'HouseID':house.HouseID})
            infolist.append({'Housename':house.Housename})
            infolist.append({'Rent':house.Rent})
            infolist.append({'Housetype': house.Housetype})
            infolist.append({'Area': house.Area})
            infolist.append({'Floor': house.Floor})
            infolist.append({'Type': house.Type})
            infolist.append({'Floor': house.Floor})
            infolist.append({'LandlordPhone': house.LandlordPhone})
            infolist.append({'OrderDate': order.OrderDate})
            infolist.append({'DueDate': order.DueDate})
            infolist.append({'Introduction': house.Introduction})
            return JsonResponse({'infolist':infolist})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

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
                    'OrderDate': x.OrderDate,
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
                    'OrderDate': x.OrderDate,
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
                    'OrderDate': x.OrderDate,
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
                    'OrderDate': x.OrderDate,
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
            order = Order.objects.filter(UserID=user_id, pay=True)
            orderlist = []
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate': x.OrderDate,
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
            infolist = []
            infolist.append({'Mark': order.Mark})  # 订单的评分而非房源的评分
            infolist.append({'HouseID': house.HouseID})
            infolist.append({'Housename': house.Housename})
            infolist.append({'Rent': house.Rent})
            infolist.append({'Housetype': house.Housetype})
            infolist.append({'Area': house.Area})
            infolist.append({'Floor': house.Floor})
            infolist.append({'Type': house.Type})
            infolist.append({'Floor': house.Floor})
            infolist.append({'LandlordPhone': house.LandlordPhone})
            infolist.append({'OrderDate': order.OrderDate})
            infolist.append({'DueDate': order.DueDate})
            infolist.append({'Introduction': house.Introduction})
            return JsonResponse({'infolist': infolist})
        elif function_id == '9': #我要报修投诉
            
        elif function_id == '10':#查看订单详情
            work_id=querylist.get('work_id')
            work = Work.objects.filter(WorkID=work_id)
            house_id = order.HouseID
            house = House.objects.get(HouseID=house_id)
            order = Order.objects.get(HouseID=house_id)
            picture = Picture.objects.get(WorkID=work_id)
            infolist = []
            infolist.append({'HouseID': house.HouseID})
            infolist.append({'Housename': house.Housename})
            infolist.append({'Rent': house.Rent})
            infolist.append({'Housetype': house.Housetype})
            infolist.append({'Area': house.Area})
            infolist.append({'Floor': house.Floor})
            infolist.append({'Type': house.Type})
            infolist.append({'Floor': house.Floor})
            infolist.append({'LandlordPhone': house.LandlordPhone})
            infolist.append({'OrderDate': order.OrderDate})
            infolist.append({'DueDate': order.DueDate})
            infolist.append({'ComplainPic':picture.PicPath})
            infolist.append({'ComplainText':work.Description})
        elif function_id == '11':#联系师傅/客服
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

