#coding:utf-8
from backend import settings
import requests
import json
from authorization.models import User

def c2s(appid,code):
    return code2session(appid,code)

def code2session(appid,code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (appid,settings.WX_APP_SECRET,code)
    url = API + '?' + params
    response = requests.get(url=url)
    data = json.loads(response.text)
    return data

def already_authorized(request):
    is_authorized = False
    try:
        if request.session['is_authorized']:
            is_authorized = True
    except:
        pass
    return is_authorized

def get_user(request):
    if not already_authorized(request):
        raise Exception('not authorized request')
    open_id = request.session['open_id']
    user = User.objects.get(open_id=open_id)
    return user