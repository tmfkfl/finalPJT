from django.urls import path
from boardApp import views
urlpatterns = [

    path("index/", views.main),
    path("login/", views.login),
    #board List
    path("list/", views.list),


]