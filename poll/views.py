from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .models import Poll, Question, Choice, Vote
#from .utils import ObjectDetailMixin

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

#from django.contrib.auth.mixins import LoginRequiredMixin
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
#    if request.method == "POST":
#        print(request.POST)
#        print("POSTED!!!!")
#        print(poll.slug)
    return render(request, 'poll/poll_detail.html', context={'poll': poll})


def poll_vote(request, slug):
    #print(request.POST)
    answer_id = request.POST.get('choice')
    poll = Poll.objects.get(slug__iexact=slug)
    if answer_id:
    #    print(answer_id) #19
        answer = Choice.objects.get(id=answer_id)
    #    print(answer)    #Yes, I celebrate
#        poll = Poll.objects.get(slug__iexact=slug)
        answer.is_answered += 1
        answer.save()
#        return HttpResponse('Slug is {}'.format(slug)) #Slug is cars-url
#        return render(request, 'poll/poll_result.html', {'poll': poll})
#    return HttpResponse("No answer choiced!")
    else:
        messages.error(request, 'No answer choiced!')
        return render(request, 'poll/poll_detail.html', context={'poll': poll})
    return render(request, 'poll/poll_result.html', {'poll': poll})