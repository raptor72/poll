from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from .models import Poll#, Question, Choice, Vote
from .utils import PollDetailMixin

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.urls import reverse
from django.contrib import messages

from django.views import generic


class IndexView(generic.ListView):
    template_name='poll/index.html'
    context_object_name='polls'

    def get_queryset(self):
        return Poll.objects.all()


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

