from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('checker_base.urls')),
    path('', include('checker_web.urls')),
]
