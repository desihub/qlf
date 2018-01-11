from django.contrib import admin
from .models import Job, Exposure, Camera, QA

admin.site.register(Job)
admin.site.register(Exposure)
admin.site.register(Camera)
admin.site.register(QA)
