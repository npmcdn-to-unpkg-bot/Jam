from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Favorite_Album(models.Model):
	AristName = models.CharField(max_length=255)
	AlbumTitle = models.CharField(max_length=255)
	MyReview = models.TextField()
	CoverURL = models.URLField()
	
	def __unicode__(self): return u'%s: %s' % (self.AristName, self.AlbumTitle)
	

