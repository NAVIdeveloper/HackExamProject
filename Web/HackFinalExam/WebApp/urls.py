from django.urls import path
from .views import *


urlpatterns = [
    path('webhook/<bot_token>/',TelegramBot_Webhook),
    path('api/create/',Api_Create_Question),
    path('api/get/<query>/',Api_Get_Answer),
    path('',DownloadFile)
]
