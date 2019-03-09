from django.shortcuts import render


# Create your views here.

def polls_list(request):
    n = ['Maksim', 'Lubov', 'Vasya', 'Wolf']
    return render(request, 'poll/index.html', context={'names': n})

