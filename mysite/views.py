from django.shortcuts import render
from django.http import  Http404, HttpResponse
from time import gmtime, strftime
from collections import deque
from PIL import Image
from jam.models import Favorite_Album
import datetime
import pitchfork
import urllib


# TEST RESPONSE
# def hello(request):
#     return HttpResponse("Hello world")

def current_datetime(request):
    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    page_title = "Evan"
    pic_url = urllib.urlopen("https://farm2.staticflickr.com/1627/24943678040_d9637bdeee_c.jpg")
    return render(request, 'time.html', {'current_time': now, 'page_title': page_title})

def lets_jam(request):
    Favorite_Album.objects.order_by("AristName")
    favAlbums = Favorite_Album.objects.all()
    # place albums in variables
    
    # Testing: 
    # Extracting Values from Favorite_Album Object
    # & Passing them into lets_jam.html Template
    addedHTML = ''
    for album in favAlbums:
        addedHTML += album.artist() + ': '
        addedHTML += album.albumTitle()

    # Dynamic Version
    favAlbumsList = list()
    for album in favAlbums:
        favAlbumsList.append(album.artist() + ': ' + album.albumTitle())


    return render(request, 'lets_jam.html', {'Albums': addedHTML, 'favAlbums': favAlbumsList})

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render(request, 'hours_ahead.html', {'hour_offset': offset, 'next_time': dt})

def evan(request):
    return render(request, 'evan.html')


    