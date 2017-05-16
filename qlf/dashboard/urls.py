from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from . import views

admin.site.site_header = 'QLF Admin'

api_router = DefaultRouter()
api_router.register(r'job', views.JobViewSet)
api_router.register(r'process', views.ProcessViewSet)
api_router.register(r'configuration', views.ConfigurationViewSet)
api_router.register(r'qa', views.QAViewSet)
api_router.register(r'exposure', views.ExposureViewSet)
api_router.register(r'camera', views.CameraViewSet)
api_router.register(r'qa-snr', views.QaSnrAppViewSet, base_name='qa-snr')

urlpatterns = [
    url(r'^dashboard/admin', include(admin.site.urls)),
    url(r'^dashboard/api/', include(api_router.urls)),
    url(r'^$', views.index, name='index')
]
