from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from . import views
from ui_channel import views as WebsocketView

admin.site.site_header = 'QLF Admin'

api_router = DefaultRouter()
api_router.register(r'job', views.JobViewSet)
api_router.register(r'process', views.ProcessViewSet)
api_router.register(r'exposure', views.ExposureViewSet)
api_router.register(r'camera', views.CameraViewSet)
api_router.register(r'qa', views.QAViewSet)
api_router.register(r'last_process', views.LastProcessViewSet, 'monitor')
api_router.register(r'datatable_exposures', views.DataTableExposureViewSet, 'datatable_exposures')
api_router.register(r'distinct_flavors',
                    views.DistinctFlavorsViewSet, 'distinct_flavors')
api_router.register(r'processing_history', views.ProcessingHistoryViewSet, 'processing_history')
api_router.register(r'observing_history', views.ObservingHistoryViewSet, 'observing_history')
api_router.register(r'qlconfig', views.QlConfigViewSet, 'qlconfig')
api_router.register(r'configuration', views.ConfigurationViewSet)
api_router.register(r'current_configuration',
                    views.CurrentConfigurationViewSet, 'current_configuration')
api_router.register(r'set_configuration',
                    views.SetConfigurationViewSet,
                    'set_configuration')
api_router.register(r'default_configuration',
                    views.DefaultConfigurationViewSet, 'default_configuration')
api_router.register(r'qa', views.QAViewSet)
api_router.register(r'exposure', views.ExposureViewSet)
api_router.register(r'datatable_exposures', views.DataTableExposureViewSet, 'datatable_exposures')
api_router.register(r'camera', views.CameraViewSet)
api_router.register(r'exposures_date_range',
                    views.ExposuresDateRangeViewSet, 'exposures_date_range')
api_router.register(r'load_scalar_metrics',
                    views.LoadScalarMetricsViewSet, 'load_scalar_metrics')
api_router.register(r'add_exposure', views.AddExposureViewSet, 'add_exposure')
api_router.register(r'current_process',
                    views.CurrentProcessViewSet, 'current_process')

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^start', views.start, name='start'),
    url(r'^stop', views.stop, name='stop'),
    url(r'^reset', views.reset, name='reset'),
    url(r'^send_ticket_email', views.send_ticket_email, name='send_ticket_email'),
    url(r'^send_message', WebsocketView.send_message, name='send_message'),
    url(r'^daemon_status', views.daemon_status, name='daemon_status'),
    url(r'^run_manual_mode', views.run_manual_mode, name='run_manual_mode'),
    url(r'^dashboard/admin', include(admin.site.urls)),
    url(r'^dashboard/api/', include(api_router.urls)),
    url(r'^dashboard/(?P<bokeh_app>\w+)/$', views.embed_bokeh, name='embed-bokeh'),
    url(r'^dashboard/observing_history', views.observing_history, name='observing_history')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls)),] + urlpatterns

