from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from gps.models import Dataset

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=Dataset.objects.order_by('-start')[:5],
            context_object_name='latest_dataset_list',
            template_name='gps/index.html')),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Dataset,
            template_name='gps/detail.html')),
    url(r'^chart/$','gps.views.chart'),
    url(r'^latest/(?P<quantity>\d+)/$','gps.views.latest'
        # DetailView.as_view(
        #     model=Dataset,
        #     template_name='gps/results.json'),
        # name='latest_datums'),
    ),
)