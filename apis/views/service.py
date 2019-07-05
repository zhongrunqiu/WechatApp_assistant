import json
import os
import random

from django.http import HttpRequest, JsonResponse
from django.views import View
from django.core.cache import cache

import thirdparty.juhe
from backend import settings
from utils.auth import User, already_authorized
from utils.response import CommonResponseMixin
from utils.timeoutUtil import get_day_left_in_second

popular_stocks = [
    {
        'code' : '000001',
        'name' : '平安银行',
        'market' : 'sz',
    },
    {
        'code' : '000002',
        'name' : '万科A',
        'market' : 'sz',
    },
    {
        'code' : '600036',
        'name' : '招商银行',
        'market' : 'sh',
    },
    {
        'code' : '601398',
        'name' : '工商银行',
        'market' : 'sh',
    },
]

all_constellations = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']

all_jokes = []

class Stock(View,CommonResponseMixin):
    def get(self,request):
        if already_authorized(request):
            user = get_user(request)
            stocks = json.loads(user.focus_stocks)
        else:
            stocks = popular_stocks
        data = []
        for stock in stocks:
            result = thirdparty.juhe.stock(stock['market'],stock['code'])
            data.append(result)
        response = self.wrap_json_response(data=data)
        return JsonResponse(data=response,safe=False)

class Constellation(View,CommonResponseMixin):
    def get(self,request):
        if already_authorized(request):
            user = get_user(request)
            constellations = json.loads(user.focus_constellations)
        else:
            constellations = all_constellations
        data = []
        for cons in constellations:
            key = 'constellations_' + cons
            result = cache.get(key)
            if not result:
                result = thirdparty.juhe.constellation(cons)
                timeout = get_day_left_in_second()
                print('key:',key)
                cache.set(key,result,timeout)
            data.append(result)
        response = self.wrap_json_response(data=data)
        return JsonResponse(data=response,safe=False)

class Joke(View,CommonResponseMixin):
    def get(self,response):
        global all_jokes
        if not all_jokes:
            all_jokes = json.load(open(os.path.join(settings.BASE_DIR,'resources','jokeData','jokes.json'),'r'))
        limits = 10
        joke_data = random.sample(all_jokes, limits)
        response = self.wrap_json_response(data=joke_data)
        return JsonResponse(data=response,safe=False)


def get_user(request):
    if not already_authorized:
        raise Exception('not authorized request')
    open_id = request.session['open_id']
    user = User.objects.get(open_id=open_id)
    return user