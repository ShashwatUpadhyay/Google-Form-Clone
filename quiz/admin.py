from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Choices)
admin.site.register(Question)
admin.site.register(Form)
admin.site.register(Response)
admin.site.register(ResponseAnswer)
