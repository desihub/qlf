from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from . import views

admin.site.site_header = 'QLF Admin'

api_router = DefaultRouter()
api_router.register(r'job', views.JobViewSet)
api_router.register(r'process', views.ProcessViewSet)
api_router.register(r'exposure', views.ExposureViewSet)
api_router.register(r'camera', views.CameraViewSet)
api_router.register(r'process_comment', views.ProcessCommentViewSet)
api_router.register(r'qa', views.QAViewSet)
api_router.register(r'last_process', views.LastProcessViewSet, 'monitor')
api_router.register(r'datatable_exposures',
                    views.DataTableExposureViewSet, 'datatable_exposures')
api_router.register(r'distinct_nights',
                    views.DistinctNightsViewSet, 'distinct_nights')
api_router.register(r'distinct_flavors',
                    views.DistinctFlavorsViewSet, 'distinct_flavors')
api_router.register(r'processing_history',
                    views.ProcessingHistoryViewSet, 'processing_history')
api_router.register(r'observing_history',
                    views.ObservingHistoryViewSet, 'observing_history')
api_router.register(r'qlconfig', views.QlConfigViewSet, 'qlconfig')
api_router.register(r'ql_calibration',
                    views.QlCalibrationViewSet, 'ql_calibration')
api_router.register(r'configuration', views.ConfigurationViewSet)
api_router.register(r'current_configuration',
                    views.CurrentConfigurationViewSet, 'current_configuration')
api_router.register(r'set_configuration',
                    views.SetConfigurationViewSet,
                    'set_configuration')
api_router.register(r'qa', views.QAViewSet)
api_router.register(r'exposure', views.ExposureViewSet)
api_router.register(r'datatable_exposures',
                    views.DataTableExposureViewSet, 'datatable_exposures')
api_router.register(r'camera', views.CameraViewSet)
api_router.register(r'exposures_date_range',
                    views.ExposuresDateRangeViewSet, 'exposures_date_range')
api_router.register(r'add_exposure', views.AddExposureViewSet, 'add_exposure')

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^start', views.start, name='start'),
    url(r'^stop', views.stop, name='stop'),
    url(r'^reset', views.reset, name='reset'),
    url(r'^dashboard/api/default_configuration/',
        views.default_configuration, name='default_configuration'),
    url(r'^send_ticket_email',
        views.send_ticket_email, name='send_ticket_email'),
    url(r'^dashboard/api/disk_thresholds',
        views.disk_thresholds, name='disk_thresholds'),
    url(r'^dashboard/api/edit_qlf_config/',
        views.edit_qlf_config, name='edit_qlf_config'),
    url(r'^daemon_status', views.daemon_status, name='daemon_status'),
    url(r'^run_manual_mode', views.run_manual_mode, name='run_manual_mode'),
    url(r'^dashboard/admin', include(admin.site.urls)),
    url(r'^dashboard/api/', include(api_router.urls)),
    url(r'^dashboard/fits_to_png', views.fits_to_png, name='fits_to_png'),
    url(r'^dashboard/load_qa', views.load_qa, name='load_qa'),
    url(r'^dashboard/get_camera_log', views.get_camera_log, name='get_camera_log'),
    url(r'^dashboard/(?P<bokeh_app>\w+)/$',
        views.embed_bokeh, name='embed-bokeh'),
    url(r'^dashboard/observing_history',
        views.observing_history, name='observing_history')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns
