from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from . import views
from . import views_bokeh

admin.site.site_header = 'QLF Admin'

api_router = DefaultRouter()
api_router.register(r'job', views.JobViewSet)
api_router.register(r'process', views.ProcessViewSet)
api_router.register(r'exposure', views.ExposureViewSet)
api_router.register(r'fibermap', views.FibermapViewSet)
api_router.register(r'camera', views.CameraViewSet)
api_router.register(r'process_comment', views.ProcessCommentViewSet)
api_router.register(r'last_process', views.LastProcessViewSet, 'monitor')
api_router.register(r'distinct_nights',
                    views.DistinctNightsViewSet, 'distinct_nights')
api_router.register(r'distinct_flavors',
                    views.DistinctFlavorsViewSet, 'distinct_flavors')
api_router.register(r'processing_history',
                    views.ProcessingHistoryViewSet, 'processing_history')
api_router.register(r'observing_history',
                    views.ObservingHistoryViewSet, 'observing_history')
api_router.register(r'configuration', views.ConfigurationViewSet)
api_router.register(r'current_configuration',
                    views.CurrentConfigurationViewSet, 'current_configuration')
api_router.register(r'set_configuration',
                    views.SetConfigurationViewSet,
                    'set_configuration')
api_router.register(r'exposure', views.ExposureViewSet)
api_router.register(r'camera', views.CameraViewSet)
api_router.register(r'exposures_date_range',
                    views.ExposuresDateRangeViewSet, 'exposures_date_range')
api_router.register(r'add_exposure', views.AddExposureViewSet, 'add_exposure')
api_router.register(r'qlconfig', views.QlConfigViewSet, 'qlconfig')

urlpatterns = [
    url(r'^send_ticket_email',
        views.send_ticket_email, name='send_ticket_email'),
    url(r'^dashboard/api/disk_thresholds',
        views.disk_thresholds, name='disk_thresholds'),
    url(r'^dashboard/admin', include(admin.site.urls)),
    url(r'^dashboard/api/', include(api_router.urls)),
    url(r'^dashboard/get_footprint',
        views_bokeh.get_footprint, name='get_footprint'),
    url(r'^dashboard/fits_to_png', views_bokeh.fits_to_png, name='fits_to_png'),
    url(r'^dashboard/load_series', views_bokeh.load_series, name='load_series'),
    url(r'^dashboard/load_spectra', views_bokeh.load_spectra, name='load_spectra'),
    url(r'^dashboard/footprint_object_type_count', views_bokeh.footprint_object_type_count, name='footprint_object_type_count'),
    url(r'^dashboard/load_qa', views_bokeh.load_qa, name='load_qa'),
    url(r'^dashboard/get_camera_log', views.get_camera_log, name='get_camera_log'),
    url(r'^dashboard/(?P<bokeh_app>\w+)/$',
        views_bokeh.embed_bokeh, name='embed-bokeh')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns
