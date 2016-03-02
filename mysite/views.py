from django.shortcuts import render
from django.http import  Http404, HttpResponse
import datetime
from PIL import Image
import pitchfork
from time import gmtime, strftime
import urllib


def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    #now = datetime.datetime.now()
    now1 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    page_title = "Evan"
    pic_url = urllib.urlopen("https://farm2.staticflickr.com/1627/24943678040_d9637bdeee_c.jpg")
    return render(request, 'current_datetime.html', {'current_time': now1, 'picture_url': pic_url, 'page_title': page_title})

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render(request, 'hours_ahead.html', {'hour_offset': offset, 'next_time': dt})

def evan(request):
    return render(request, 'evan.html', {})
    