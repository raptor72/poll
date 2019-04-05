from django.views.generic import View

from .models import Poll
from .utils import PollDetailMixin, PollResultMixin

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic


class IndexView(generic.ListView):
    template_name='poll/index.html'
    context_object_name='polls'

    def get_queryset(self):
        return Poll.objects.all()


class PollDetail(LoginRequiredMixin, PollDetailMixin, View):
    login_url = '/poll/login/'
    redirect_field_name = 'poll/poll_detail.html'


class PollResult(LoginRequiredMixin, PollResultMixin, View):
    model = Poll

