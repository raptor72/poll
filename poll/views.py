from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .models import Poll, Question
from .utils import ObjectDetailMixin

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

def polls_list(request):
    polls = Poll.objects.all()
    return render(request, 'poll/index.html', context={'polls': polls})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('polls_list_url'))
        else:
            messages.error(request, 'uncorrect name or password')

    return render(request, 'poll/login.html', {})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls_list_url'))

class PollDetail(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Poll
    template = 'poll/poll_detail.html'
    login_url = '/poll/login/'
    redirect_field_name = 'redirect_to'

