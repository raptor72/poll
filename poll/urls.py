from django.urls import path

from .views import *

from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', IndexView.as_view(), name='polls_list_url'),
    path('kerberos/', kerberos_test, name='polls_list_url'),
    path('kerberos2/', KerberosResult.as_view(), name='poll_result'),
    path('login/', LoginView.as_view(template_name='poll/login.html')),
    path('logout/', LogoutView.as_view()),
    path('<str:slug>/', PollDetail.as_view(), name='poll_detail_url'),
    path('<str:slug>/result/', PollResult.as_view(), name='poll_result'),
]
