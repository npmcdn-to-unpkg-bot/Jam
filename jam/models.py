from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Favorite_Album(models.Model):
	AristName = models.CharField(max_length=255)
	AlbumTitle = models.CharField(max_length=255)
	MyReview = models.TextField()
	CoverURL = models.URLField()
	
	def __unicode__(self): return u'%s: %s' % (self.AristName, self.AlbumTitle)

	def toString(self):
		return '%s: %s' % (self.AristName, self.AlbumTitle)

	def albumTitle(self):
		return '%s' % (self.AlbumTitle)

	def artist(self):
		return '%s' % (self.AristName)

	#class Meta:
    #     ordering = ['name']
	

