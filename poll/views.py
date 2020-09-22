from django.views.generic import View

from .models import Poll
from .utils import PollDetailMixin, PollResultMixin, KerberosResultMixin

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import base64
from django.http import HttpResponse
from django.contrib.auth import authenticate, login



from django.views.generic.detail import SingleObjectMixin


# def logged_in_or_basicauth(realm = ""):
#     def view_decorator(func):
#         def wrapper(request, *args, **kwargs):
#             return view_or_basicauth(func, request,
#                                      lambda u: u.is_authenticated(),
#                                      realm, *args, **kwargs)
#         return wrapper
#     return view_decorator


# @login_required(login_url='/poll/login/')
def kerberos_test(request):
    print(dir(request))
    print("############################")
    print(request.META)
    # print(request.META['HTTP_AUTHORIZATION'])
    # print(request.META.get('HTTP_AUTHORIZATION')
    polls = Poll.objects.all()
    return render(request, 'poll/index.html', context={'polls': polls})


class IndexView(generic.ListView):
    template_name='poll/index.html'
    context_object_name='polls'

    def get_queryset(self):
        return Poll.objects.all()


class PollDetail(LoginRequiredMixin, PollDetailMixin, View):
    login_url = '/poll/login/'
    redirect_field_name = 'poll/poll_detail.html'


class PollResult(LoginRequiredMixin, PollResultMixin, View):
    model = Poll


class KerberosResult(SingleObjectMixin, KerberosResultMixin, View):
    model = Poll
