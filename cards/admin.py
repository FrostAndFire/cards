from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Card)
admin.site.register(Rating)
