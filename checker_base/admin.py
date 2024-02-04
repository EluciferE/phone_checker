from django.contrib import admin

from checker_base.models import Operator, PhoneGroup, Region

admin.site.register(Operator)
admin.site.register(Region)
admin.site.register(PhoneGroup)
