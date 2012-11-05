from django.db import models
import datetime, time
from django.utils import timezone

class Dataset(models.Model):
    start = models.DateTimeField('date published')

    def __unicode__(self):
    	return str(self.start)

    def size(self):
    	pass

    
class Datum(models.Model):
  	dataset = models.ForeignKey(Dataset)
	gpsstring = models.CharField(max_length=200)
	speed = models.IntegerField()

	def __unicode__(self):
		return str(self.speed)
