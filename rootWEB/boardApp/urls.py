from django.urls import path
from boardApp import views
urlpatterns = [

    path("index/", views.main , name = 'index'),
    path("login/", views.login),
    path("joinForm/", views.joinForm),
    path("join/", views.join),
    path("logout/", views.logout),
    #board List
    path("list/", views.list, name = 'list'),
    path("bbsForm/", views.registerForm),
    path("register/", views.register),
    path("view/", views.read, name='view'),
    path("delete/", views.delete),
    path("update/", views.update),
    path("search/", views.search),

]