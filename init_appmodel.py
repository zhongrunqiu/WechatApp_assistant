import os
import django
import yaml
import hashlib

os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')
django.setup()

from backend import settings
from apis.models import App

def init_app_data():
    old_apps = App.objects.all()
    path = os.path.join(settings.BASE_DIR,'utils','app.yaml')
    with open(path,'r',encoding='utf-8') as f:
        apps = yaml.safe_load(f)
        published = apps['published']
        for item in published:
            item = item['app']
            #生成唯一id
            src = item['category'] + item['application']
            appid = hashlib.md5(src.encode('utf8')).hexdigest()

            if len(old_apps.filter(appid=appid)) == 1:
                print('already exist,appid:',appid)
                app = old_apps.get(appid=appid)
            else:
                print('not exist,creare appid:',appid)
                app = App()
            app.appid = appid
            app.category = item['category']
            app.application = item['application']
            app.name = item['name']
            app.publish_date = item['publish_date']
            app.url = item['url']
            app.desc = item['desc']
            app.save()

if __name__ == "__main__":
    init_app_data()