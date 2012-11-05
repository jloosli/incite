from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from gps.models import Dataset, Datum
from django.http import Http404
from django.db.models import Max
import json
# Create your views here.

def latest(request, quantity=100):
	#latest = Dataset.objects.latest('start')
	latest = Dataset.objects.order_by('-id')[:1][0].id
	data=Datum.objects.filter(dataset__pk=latest).order_by('id')
	formatted = map(lambda x:float(x.speed) if x.speed else 0, data)

	return render_to_response('gps/results.json',{'data' : json.dumps(formatted [-1 * int(quantity) :])})

def chart(request):
	return render_to_response('gps/chart.html')
