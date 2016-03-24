from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Artists(models.Model):
	ArtistName = models.CharField(max_length=255)
	SpotifyID = models.CharField(primary_key=True, max_length=255)
	PrimaryGenre = models.CharField(max_length=255)
	SecondaryGenre = models.CharField(max_length=255)
	
	def __unicode__(self): return u'%s' % (self.ArtistName)
	def toString(self):
		return '%s' % (self.ArtistName)
	def artistID(self):
		return '%s' % (self.SpotifyID)

	#class Meta:
    #     ordering = ['name']
	
class Album(models.Model):
	AlbumTitle = models.CharField(max_length=255)
	SpotifyAlbumID = models.CharField(max_length=255, default=1)
	ArtistID = models.ForeignKey(Artists, on_delete=models.CASCADE)
	Favorite = models.IntegerField(default=0)

	def __unicode__(self): return u'%s' % (self.AlbumTitle)
	def toString(self):
		return '%s' % (self.AlbumTitle)
	def Album(self):
		return '%s' % (self.AlbumTitle)
	def isFavorite(self):
		return Favorite

