from django_filters import rest_framework as filters
from .models import Process


class ProcessingHistoryFilter(filters.FilterSet):
    ''' filter on Processing History fields '''
    end__isnull = filters.BooleanFilter(name='end', lookup_expr='isnull')

    class Meta:
        model = Process
        fields = (
          'exposure_id',
          'exposure__tile',
          'exposure__telra',
          'exposure__night',
          'exposure__exptime',
          'exposure__flavor',
          'exposure__program',
          'exposure__dateobs',
          'exposure__airmass',
          'exposure__teldec',
          'end__isnull',
          'end',
          'status')
