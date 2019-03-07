from django.urls import path

from .views import *


urlpatterns = [
    path('', polls_list)
]
