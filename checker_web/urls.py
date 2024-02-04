from django.urls import path

from checker_web.views import index

urlpatterns = [
    path('', index, name='index'),
]
