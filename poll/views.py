from django.views.generic import View

from .models import Poll
from .utils import PollDetailMixin, PollResultMixin, KerberosResultMixin

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic

from django.shortcuts import render
from django.template.response import TemplateResponse

from django.views.generic.detail import SingleObjectMixin




def kerberos_test(request):
    # print(dir(request))
    print("############################")
    # print(request.META)
    # print(request.META['HTTP_AUTHORIZATION'])
    # print(request.META.get('HTTP_AUTHORIZATION')
    polls = Poll.objects.all()
    if 'HTTP_AUTHORIZATION' in request.META:
        print(request.META)
        print("Auth complite")
#    request headers={"WWW-Authenticate": "Negotiate; charset=utf-8"}
    else:
        unauthorized_template_name = 'poll/unauthorized.html'
        response = TemplateResponse(request, 'poll/unauthorized.html', status=401)
        # response =  render(request, 'poll/index.html', context={'polls': polls})
        response["WWW-Authenticate"] = "Negotiate"
        return response
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
