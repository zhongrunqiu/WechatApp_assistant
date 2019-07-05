from django.shortcuts import render
from django.http import JsonResponse
from utils.response import CommonResponseMixin,ReturnCode
from utils.auth import c2s,already_authorized
from django.views import View
import json
from .models import User

# Create your views here.

def test_session(request):
    request.session['message'] = 'Test Django Session OK'
    response = CommonResponseMixin.wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response,safe=False)

def test_session2(request):
    print('session content:',request.session.items())
    response = CommonResponseMixin.wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response,safe=False)

class UserStatus(View,CommonResponseMixin):
    def get(self,request):
        if already_authorized(request):
            status = {
                'is_authorized' : True
            }
        else:
            status = {
                'is_authorized' : False
            }
        response = self.wrap_json_response(data=status)
        return JsonResponse(data=response,safe=False)

class UserView(View,CommonResponseMixin):
    def get(self,request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.SUCCESS)
            return JsonResponse(data=response,safe=False)
        open_id = request.session['open_id']
        user = User.objects.get(open_id=open_id)
        data = {}
        data['focus'] ={}
        data['focus']['city'] = json.loads(user.focus_cities)
        data['focus']['constellation'] = json.loads(user.focus_constellations)
        data['focus']['stock'] = json.loads(user.focus_stocks)
        response = self.wrap_json_response(data=data,code=ReturnCode.SUCCESS)
        return JsonResponse(data=response,safe=False)

    def post(self,request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.SUCCESS)
            return JsonResponse(data=response,safe=False)
        open_id = request.session['open_id']
        user = User.objects.get(open_id=open_id)
        received_data = request.body.decode('utf-8')
        print('1:',received_data)
        received_data = eval(received_data)
        print(received_data)
        focus_cities = received_data['city']
        focus_constellations = received_data['constellation']
        focus_stocks = received_data['stock']

        user.focus_cities = json.dumps(focus_cities)
        user.focus_constellations = json.dumps(focus_constellations)
        user.focus_stocks = json.dumps(focus_stocks)
        user.save()

        response = self.wrap_json_response(message='modify userinfo success')
        return JsonResponse(data=response,safe=False)

class LoginOut(View,CommonResponseMixin):
    def get(self,request):
        request.session.clear()
        response = self.wrap_json_response(message='logout seccess')
        return JsonResponse(data=response,safe=False)

def __authorize_by_code(request):
    '''
    使用wx.login得到的临时code到微信提供code2session接口授权
    '''
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    code = post_data['code'].strip()
    app_id = post_data['appId'].strip()
    nickname = post_data['nickname'].strip()

    if not code or not app_id:
        response['message'] = 'authorized failed,need entire authorization data'
        response['code'] = ReturnCode.BROKEN_AUTHORIZED_DATA
        return JsonResponse(data=response,safe=False)
    data =c2s(app_id,code)
    openid = data['openid']
    if not openid:
        response = CommonResponseMixin.wrap_json_response(code=ReturnCode.FAILED,message='auth failed')
        return JsonResponse(data=response,safe=False)

    request.session['open_id'] = openid
    request.session['is_authorized'] = True

    if not User.objects.filter(open_id=openid):
        new_user = User(open_id=openid,nickname=nickname)
        new_user.save()

    response = CommonResponseMixin.wrap_json_response(code=ReturnCode.SUCCESS,message='auth success')
    return JsonResponse(data=response,safe=False)


def authorize(request):
    return __authorize_by_code(request)
