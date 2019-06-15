from django.contrib import admin
from django.urls import path
from .views import weather,menu,image,service

urlpatterns = [
    # path('weather', weather.weather),
    path('weather', weather.WeatherView.as_view()),
    path('menu',menu.get_menu),
    # path('image',image.image),
    # path('imagetext',image.image_text)
    path('image',image.ImageView.as_view()),
    path('image/list',image.ImageListView.as_view()),
    path('stock',service.Stock.as_view()),
    path('constellation',service.Constellation.as_view()),
    path('joke',service.Joke.as_view())
]