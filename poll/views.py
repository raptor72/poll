from django.shortcuts import render

from .models import Poll, Question

# Create your views here.

def polls_list(request):
    polls = Poll.objects.all()
    return render(request, 'poll/index.html', context={'polls': polls})


def poll_detail(request, slug):
    poll = Poll.objects.get(slug__iexact=slug)
    return render(request, 'poll/poll_detail.html', context={'poll': poll})
