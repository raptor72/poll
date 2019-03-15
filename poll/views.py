from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .models import Poll, Question, Choice, Vote

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django.contrib.auth.decorators import login_required

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

@login_required(login_url='/poll/login/')
def poll_detail(request, slug):
    poll = Poll.objects.get(slug__iexact=slug)
    return render(request, 'poll/poll_detail.html', context={'poll': poll})


def poll_vote(request, slug):
    #print(request.POST)
    answer_id = request.POST.get('choice')
    poll = Poll.objects.get(slug__iexact=slug)
    if answer_id:
        answer = Choice.objects.get(id=answer_id)
        answer.is_answered += 1
        answer.save()
    else:
        messages.error(request, 'No answer choiced!')
        return render(request, 'poll/poll_detail.html', context={'poll': poll})
    return render(request, 'poll/poll_result.html', {'poll': poll})