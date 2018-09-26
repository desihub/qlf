from django.contrib import admin
from .models import Job, Exposure, Camera, ProcessComment

admin.site.register(Job)
admin.site.register(Exposure)
admin.site.register(Camera)
admin.site.register(ProcessComment)
