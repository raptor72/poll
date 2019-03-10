from django.urls import path

from .views import *


urlpatterns = [
    path('', polls_list, name='polls_list_url'),
#    path('poll/<str:slug>/', poll_detail, name = 'poll_detail_url')
    path('<str:slug>/', poll_detail, name = 'poll_detail_url')
]
