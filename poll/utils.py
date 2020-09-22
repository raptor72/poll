from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import *


from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse


class PollDetailMixin:
    model = Poll
    template = 'poll/poll_detail.html'

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        user_can_vote = obj.user_can_vote(request.user)
        return render(request, self.template, context={self.model.__name__.lower(): obj,
                                                       'user_can_vote': user_can_vote})

    def post(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        if not obj.user_can_vote(request.user):
            messages.error(request, 'You are already voted')
            return render(request, self.template, context={self.model.__name__.lower(): obj})
        all_questions = len(obj.question_set.all())
        send_questions = []
        question_set = set()
        for i in request.POST.items():
            if 'choice' in i[0]:
                send_questions.append(i[1])
            for j in send_questions:
                answer_id = j
                question_id = Choice.objects.get(id=answer_id).question.id
                question_set.add(question_id)
        if len(send_questions) != all_questions or len(question_set) != all_questions:
            messages.error(request, 'You should choose one answer in each question')
            return redirect('poll_detail_url', slug=obj.slug)
        else:
            for i in send_questions:
                answer_id = i
                answer = Choice.objects.get(id=answer_id)
                new_vote = Vote(user=request.user, poll=obj, choice=answer)
                new_vote.save()
            return redirect('poll_detail_url', slug=obj.slug)


class PollResultMixin:
    model = None
    template = 'poll/poll_result.html'

    def get(self, request, slug):
        obj = get_object_or_404(Poll, slug__iexact=slug)
        superuser = request.user.is_superuser
        if superuser is False:
            messages.error(request, 'You are not admin')
            return redirect('poll_detail_url', slug=obj.slug)
        else:
            return render(request, self.template, context={self.model.__name__.lower(): obj})


class KerberosResultMixin:
    model = None
    template = 'poll/poll_list_url.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        print(request.META)
        polls = model.objects.all()
        return render(request, 'poll/index.html', context={'polls': polls})
        


