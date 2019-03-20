from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from .models import Poll#, Question, Choice, Vote
from .utils import PollDetailMixin

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


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
            messages.error(request, 'uncorrected name or password')
    return render(request, 'poll/login.html', {})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls_list_url'))


class PollDetail(LoginRequiredMixin, PollDetailMixin, View):
    login_url = '/poll/login/'
    redirect_field_name = 'poll/poll_detail.html'


def poll_result(request, slug):
    poll = get_object_or_404(Poll, slug__iexact=slug)
    superuser = request.user.is_superuser
    if superuser is False:
        messages.error(request, 'You are not admin')
        return redirect('poll_detail_url', slug=poll.slug)
    else:
        return render(request, 'poll/poll_result.html', {'poll': poll})


def user_results(request):
    superuser = request.user.is_superuser
    if superuser is False:
        messages.error(request, 'You are not admin')
        return redirect('polls_list_url')
    else:
        user = User.objects.all()
        for i in user:
            print(i.vote_set.all())
        return render(request, 'poll/user_results.html', {'user': user})

