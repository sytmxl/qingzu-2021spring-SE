from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

'''
主界面网站：
根据用户的点击，选择跳转的网站
'''
@csrf_exempt
def index(request):

    return JsonResponse()
@csrf_exempt
def houseinfo(request,house_id):

    return JsonResponse()
@csrf_exempt
def housetrade(request,house_id):

    return JsonResponse()