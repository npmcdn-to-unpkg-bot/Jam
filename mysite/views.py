from django import template
from django.shortcuts import get_object_or_404, render
from django.http import  Http404, HttpResponse, JsonResponse
from time import gmtime, strftime
import datetime
import urllib
import urllib2

###########################
#    GENERAL PAGE FUNCTIONS
###########################

def current_datetime(request):
    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    page_title = "Evan"
    pic_url = urllib.urlopen("https://farm2.staticflickr.com/1627/24943678040_d9637bdeee_c.jpg")
    return render(request, 'time.html', {'current_time': now, 'page_title': page_title})

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render(request, 'hours_ahead.html', {'hour_offset': offset, 'next_time': dt})

def evan(request):
    with open('jam/static/__resume__.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        pdf.closed
        return response

###################
#  HELPER FUNCTIONS
###################

def spotify_gen_search(recommened_item):
    spotify_Search_response_album = urllib2.urlopen('https://api.spotify.com/v1/search?q=' + convert_to_query(recommened_item) + '&type=album&market=US')
    json_Search_response_album = json.load(spotify_Search_response_album)
    spotify_Search_response_artist = urllib2.urlopen('https://api.spotify.com/v1/search?q=' + convert_to_query(recommened_item) + '&type=artist&market=US')
    json_Search_response_artist = json.load(spotify_Search_response_artist)
    return json_Search_response_artist, json_Search_response_album

def url_argument_parse(album):
    title = ''
    frontOfString = 0
    for character in range(len(album)):
        if (album[character] == '_'):
            title += album[frontOfString:character]
            title += ' '
            frontOfString = character+1
        elif(character == len(album)-1):
            title += album[frontOfString:]
    return title

def convert_to_query(album_title):
    queryTitle = ''
    for character in range(len(album_title)):
        if album_title[character] == ' ':
            queryTitle += '+'
        else:
            queryTitle += album_title[character]
    return queryTitle

######################
# DEPRICATED FUNCTIONS
######################

    