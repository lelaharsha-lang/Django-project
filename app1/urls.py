from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'app1'

urlpatterns = [
    path('about/',views.about,name='about'),
    path('add/',views.add,name='add'),
    path('loginn/',views.loginn,name='loginn'),
    path('button/',views.button,name='button'),
    path('button/page',views.page,name='page'),
]