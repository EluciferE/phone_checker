from django.urls import path

from checker_base.views import api

urlpatterns = [
    path('phone_info', api.get_phone_info, name='get-phone-info'),
]
