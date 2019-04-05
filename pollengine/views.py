from django.http import HttpResponse
from django.shortcuts import redirect

def redirect_poll(request):
    return redirect('polls_list_url', permanent=True)
