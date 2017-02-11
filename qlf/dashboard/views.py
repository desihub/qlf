from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.views.decorators.csrf import ensure_csrf_cookie

import json

from rest_framework import authentication, permissions, viewsets
from .models import Job, Metric
from .serializers import JobSerializer, MetricSerializer

from bokeh.embed import autoload_server


class DefaultsMixin(object):
    """
    Default settings for view authentication, permissions,
    filtering and pagination.
    """

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
        permissions.IsAuthenticated,
    )

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100


class JobViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating jobs"""

    queryset = Job.objects.order_by('name')
    serializer_class = JobSerializer


class MetricViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating metrics"""

    queryset = Metric.objects.order_by('name')
    serializer_class = MetricSerializer

@ensure_csrf_cookie
def index(request):
    return render_to_response('index.html')
