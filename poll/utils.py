from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

from .models import *


class ObjectDetailMixin:
    model = None
    template = None
    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        user_can_vote = obj.user_can_vote(request.user)
        return render(request, self.template, context={self.model.__name__.lower(): obj, 'user_can_vote': user_can_vote})


class PollVoteMixin:
    model = None
    template = None
    def post(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        user_can_vote = obj.user_can_vote(request.user)
        if not obj.user_can_vote(request.user):
            messages.error(request, 'You are already voted')
            return render(request, self.template, context={self.model.__name__.lower(): obj})
        all_questions = len(obj.question_set.all())
        send_questions = []
        for i in request.POST.items():
            if 'choice' in i[0]:
                send_questions.append(i[1])
        if len(send_questions) != all_questions:
            messages.error(request, 'You should choose all answers')
            return redirect('poll_detail_url', slug=obj.slug)
#            return render(request, self.template, context={self.model.__name__.lower(): obj})
        else:
            for i in send_questions:
                answer_id = i
                answer = Choice.objects.get(id=answer_id)
                new_vote = Vote(user=request.user, poll=obj, choice=answer)
                new_vote.save()
            return redirect('poll_detail_url', slug=obj.slug)
#            return render(request, self.template, context={self.model.__name__.lower(): obj})
