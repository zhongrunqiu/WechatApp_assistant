from django.http import HttpRequest,HttpResponse,JsonResponse
from thirdparty import juhe
import json
import utils.response
from django.views import View
from utils.auth import User,already_authorized

def helloworld(request):
    print('request method:',request.method)
    print('request META:',request.META)
    print('request cookies:',request.COOKIES)
    print('request QueryDict:',request.GET)
    # data = 'Hello Django Response!'
    data = {
        'message':'Hello Django Response!'
    }
    # return HttpResponse(content=data,status=200)
    return JsonResponse(data=data,safe=False,status=200)

def weather(request):
    if request.method == 'GET':
        city = request.GET.get('city')
        data = juhe.weather(city)
        return JsonResponse(data=data,safe=False,status=200)
    elif request.method == 'POST':
        recived_body = request.body
        recived_body = json.loads(recived_body)
        cities = recived_body['cities']
        response_data = []
        for item in cities:
            province = item['province']
            city = item['city']
            area = item['area']
            query = area + ',' + city + ',' + province
            result = juhe.weather(query)
            response_data.append(result)
        return JsonResponse(data=response_data,safe=False,status=200)

class WeatherView(View,utils.response.CommonResponseMixin):
    def get(self,request):
        if not already_authorized(request):
            response = self.wrap_json_response({},utils.response.ReturnCode.UNAUTHORIZED)
        else:
            data = []
            open_id = request.session['open_id']
            print(open_id)
            user = User.objects.get(open_id=open_id)
            cities = json.loads(user.focus_cities)
            for city in cities:
                result = juhe.weather(city['city'],city['area'])
                data.append(result)
            response = self.wrap_json_response(data=data)
        return JsonResponse(response,safe=False)
    def post(self,request):
        recived_body = request.body.decode('utf-8')
        recived_body = json.loads(recived_body)
        cities = recived_body['cities']
        response_data = []
        for item in cities:
            province = item['province']
            city = item['city']
            area = item['area']
            print('province:',province,'city:',city,'area:',area)
            result = juhe.weather(city,area)
            response_data.append(result)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response,safe=False)