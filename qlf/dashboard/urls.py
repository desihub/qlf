from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from . import views

api_router = DefaultRouter()
api_router.register(r'job', views.JobViewSet)
api_router.register(r'metric', views.MetricViewSet)

urlpatterns = [
    url(r'^dashboard/admin', include(admin.site.urls)),
    url(r'^dashboard/api/', include(api_router.urls)),
    url(r'^dashboard/api/token/', obtain_auth_token, name='api-token'),
    url(r'^(?P<pk>[a-zA-Z0-9]*$)', views.MetricView.as_view(),
        name='module-list'),
]
