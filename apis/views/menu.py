import os
import yaml
from backend import settings
from django.http import JsonResponse
from utils.response import CommonResponseMixin,ReturnCode
from utils.auth import already_authorized,get_user
from django.views import View
from authorization.models import User
from apis.models import App
import json

def init_app_data():
    data_file = os.path.join(settings.BASE_DIR,'utils/app.yaml')
    with open(data_file,'r',encoding='utf-8') as f:
        apps = yaml.load(f)
        return apps

# def get_menu(request):
#     global_app_data = init_app_data()
#     published_app_data = global_app_data.get('published')
#     response = utils.response.wrap_json_response(data=published_app_data,code=utils.response.ReturnCode.SUCCESS)
#     return JsonResponse(response,safe=False)

class MenuView(View,CommonResponseMixin):
    def get(self,request):
        if not already_authorized(request):
            # global_app_data = init_app_data()
            # published_app_data = global_app_data.get('published')
            query_set = App.objects.all()
            all_app = []
            for app in query_set:
                all_app.append(app.to_dict())
            response = self.wrap_json_response(data=all_app,code=ReturnCode.SUCCESS)
            return JsonResponse(response,safe=False)
        else:
            user = get_user(request)
            menu_list = user.menu.all()
            print(menu_list,type(menu_list))
            user_menu = []
            for app in menu_list:
                user_menu.append(app.to_dict())
            response = self.wrap_json_response(data=user_menu,code=ReturnCode.SUCCESS)
            print('user_menu:',user_menu)
            return JsonResponse(response,safe=False)

    def post(self,request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(data=response,safe=False)
        user = get_user(request)
        post_menu = json.loads(request.body.decode('utf-8'))
        post_menu = post_menu['data']
        focus_menu = []
        for item in post_menu:
            item = App.objects.get(appid=item['appid'])
            focus_menu.append(item)
        user.menu.set(focus_menu)
        user.save()
        response = self.wrap_json_response()
        return JsonResponse(data=response,safe=False)