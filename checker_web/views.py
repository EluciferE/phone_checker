from django.shortcuts import render


def index(request):
    return render(request, 'checker_web/index.html')
