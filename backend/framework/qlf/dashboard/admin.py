from django.contrib import admin
from .models import Job, Exposure, Camera, QA, ProcessComment

admin.site.register(Job)
admin.site.register(Exposure)
admin.site.register(Camera)
admin.site.register(QA)
admin.site.register(ProcessComment)
