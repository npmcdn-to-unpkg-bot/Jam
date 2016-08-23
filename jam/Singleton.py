# Singleton.py

from jam.models import Artists, Album

class Singleton(type):
	_instances = {}
	def __init__(cls, name):
		if cls not in cls._instances:
            cls._instances[cls] = super.__call__(*args, **kwargs)
         return cls._instances[cls]

	def __call__(cls):
        return cls._instances[cls];

class Cache(object, metaclass = Singleton):
	def __init__(self, className):
		super.__init__(self, className, {"albums" : set(), "artists" : set(), "reviews": set()})

    def __call__(self):
        return super.__call__(self)

	def searchArtist(self, name):
		artistCache = self.__call__().artists
        if artistCache[name]:
            return artistCache[name]
        return readThrough(artistCache, name)

    def searchAlbum(self, name):
        albumCache = self.__call__().albums
        if albumCache[name]:
            return albumCache[name]
        return readThrough(albumCache, name)
	
	def readThrough(cacheSet, replacement):
		pass

