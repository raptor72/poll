from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .models import Poll, Question
from .utils import ObjectDetailMixin

# Create your views here.

def polls_list(request):
    polls = Poll.objects.all()
    return render(request, 'poll/index.html', context={'polls': polls})

class PollDetail(ObjectDetailMixin, View):
    model = Poll
    template = 'poll/poll_detail.html'


