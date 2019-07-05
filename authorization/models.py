from django.db import models
from apis.models import App

# Create your models here.

class User(models.Model):
    #openid为唯一的开启唯一
    open_id = models.CharField(max_length=32,unique=True)
    #昵称
    nickname = models.CharField(max_length=256)
    #关心的城市
    focus_cities = models.TextField(default=[])
    #关心的星座
    focus_constellations = models.TextField(default=[])
    #关心的股票
    focus_stocks = models.TextField(default=[])
    #与App建立多对多关系
    menu = models.ManyToManyField(App)

    class Meta:
        indexes = [
            models.Index(fields=['nickname']),
            models.Index(fields=['open_id']),
        ]

    def __str__(self):
        return self.nickname