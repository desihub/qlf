from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from . import views

admin.site.site_header = 'QLF Admin'

api_router = DefaultRouter()
api_router.register(r'job', views.JobViewSet)
api_router.register(r'process', views.ProcessViewSet)
api_router.register(r'last_process', views.LastProcessViewSet, 'monitor')
api_router.register(r'configuration', views.ConfigurationViewSet)
api_router.register(r'qa', views.QAViewSet)
api_router.register(r'exposure', views.ExposureViewSet)
api_router.register(r'camera', views.CameraViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^start', views.start, name='start'),
    url(r'^stop', views.stop, name='stop'),
    url(r'^dashboard/nightsum', views.exposureList,  name='exposureList'),
    url(r'^restart', views.restart, name='restart'),
    url(r'^dashboard/admin', include(admin.site.urls)),
    url(r'^dashboard/api/', include(api_router.urls)),
    url(r'^dashboard/(?P<bokeh_app>\w+)/$', views.embed_bokeh,
        name='embed-bokeh')
]
