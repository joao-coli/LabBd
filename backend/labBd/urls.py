from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.index, name='home'),
    path('user/', views.index, name="user"),
    path('', views.index, name="index")

]