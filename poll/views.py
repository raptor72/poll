from django.shortcuts import render, redirect, get_object_or_404
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
    poll = get_object_or_404(Poll, slug__iexact=slug)
    user_can_vote = poll.user_can_vote(request.user)
    return render(request, 'poll/poll_detail.html', context={'poll': poll, 'user_can_vote': user_can_vote})

def poll_vote(request, slug):
    poll = get_object_or_404(Poll, slug__iexact=slug)
    if not poll.user_can_vote(request.user):
        messages.error(request, 'You are already voted')
        return render(request, 'poll/poll_detail.html', context={'poll': poll})
    all_questions = len(poll.question_set.all())
    send_questions = []
    for i in request.POST.items():
        if 'choice' in i[0]:
            send_questions.append(i[1])
    if len(send_questions) != all_questions:
            messages.error(request, 'You should chioce all answers')
#            return render(request, 'poll/poll_detail.html', context={'poll': poll})
            return redirect('poll_detail_url', slug=poll.slug)
    else:
        for i in send_questions:
            answer_id = i
            answer = Choice.objects.get(id=answer_id)
            new_vote = Vote(user=request.user, poll=poll, choice=answer)
            new_vote.save()
#        return render(request, 'poll/poll_result.html', {'poll': poll})
        return redirect('poll_detail_url', slug=poll.slug)


def poll_result(request, slug):
    poll = get_object_or_404(Poll, slug__iexact=slug)
    superuser = request.user.is_superuser
    if superuser is False:
        messages.error(request, 'You are not admin')
        return redirect('poll_detail_url', slug=poll.slug)
    else:
        return render(request, 'poll/poll_result.html', {'poll': poll})

