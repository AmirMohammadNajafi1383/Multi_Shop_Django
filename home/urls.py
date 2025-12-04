from django.urls import path
from . import views

ap_name = 'home'
urlpatterns = [
    path('',views.Home.as_view(),name='home')
]