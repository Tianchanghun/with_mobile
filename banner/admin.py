from django.contrib import admin
from .models import Mainbanner, subbanner

# Register your models here.
admin.site.register(subbanner)
admin.site.register(Mainbanner)

