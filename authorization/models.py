from django.db import models

# Create your models here.

class User(models.Model):
    #openid为唯一的开启唯一
    open_id = models.CharField(max_length=32,unique=True)
    #昵称
    nickname = models.CharField(max_length=256)
    #
    focus_cities = models.TextField(default=[])

    focus_constellations = models.TextField(default=[])

    focus_stocks = models.TextField(default=[])