from django.contrib import admin
from django.urls import path,include
from authorization import views

urlpatterns = [
    path('test',views.test_session),
    path('test2',views.test_session2),
    path('authorize',views.authorize,name='authorize'),
    path('user',views.UserView.as_view()),
    path('status',views.UserStatus.as_view()),
]