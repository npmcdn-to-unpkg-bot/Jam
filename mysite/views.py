from django.shortcuts import get_object_or_404, render
from django.http import  Http404, HttpResponse
from time import gmtime, strftime
from collections import deque
from PIL import Image
from jam.models import Artists, Album
import datetime
import pitchfork
import urllib
import urllib2
import json

###################
#          API KEYS
###################

spotify_api_key = '509df3f3d7584069a23c2db440960b20'
spotify_api_secret = 'e3826548f35d4ecb88c4eb8032ada051'
OAuth_token = 'BQDbMT3TcgCddi2y7_NehZU54TGQBk0MXbgO9izP5WrCeO40WqLdL98j88zeQwrMIBGj9'

echonest_api_key = 'JXWIZXVWFCDBT9DVG'
echonest_consumer_key = 'd3755c57dc73a9132325cd5bac8d4556'
echonest_shared_secret = '1b5YciWYSia7H0EMMM8rLw'

###################
#    PAGE FUNCTIONS
###################

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
    return render(request, 'evan.html')

def lets_jam(request):
    # Home Page of JAM
    # Page to display Featured Favorite Albums
    all_artist = Artists.objects.all()
    print all_artist
    featured_albums = list()
    for artist in all_artist:
        featured_albums.append(Album.objects.filter(ArtistID=artist.artistID()))
    # GET ALBUM COVERS / FOR LOOP IN lets_jam.html
    return render(request, 'lets_jam.html', {'featured_albums': featured_albums})

def lets_jam_recommend(request):
    # Recommendation Page
    # try:
    #     recommened_item = question.choice_set.get(Album=request.POST['recommened_item'])
    # except (KeyError, Recommendation.DoesNotExist):
    #     # we couldn't find your recommendation
    #     # display error message
    #     return render(request, 'lets_jam_recommend.html')

    # else:

    return render(request, 'lets_jam_recommend.html')

def lets_jam_review(request, album_title):
    album_title = url_argument_parse(album_title)
    # GET_ARTIST
    # [Query DB to get Artist ID & Artist Name]
    albumSet = Album.objects.filter(AlbumTitle=album_title)
    # if empty: No Corresponding Artist / Create Artist
    if not albumSet:
        # search album title, get album ID, get artist ID
        spotify_Search_response = urllib2.urlopen('https://api.spotify.com/v1/search?q=' + convert_to_query(album_title) + '&type=album&market=US')
        json_Search_response = json.load(spotify_Search_response)
        spotify_Get_an_Album_API_response = urllib2.urlopen('https://api.spotify.com/v1/albums/' + json_Search_response['albums']['items'][0]['id'] + '?market=US')
        matched_artist = Artists.objects.filter(SpotifyID=json_Search_response['albums']['items'][0]['id'])
        if not matched_artist:
            json_Get_an_Album_API_response = json.load(spotify_Get_an_Album_API_response)
            spotify_Artist_ID = json_Get_an_Album_API_response['artists'][0]['id']
            spotify_Artist_Name = json_Get_an_Album_API_response['artists'][0]['name']
            spotify_Get_an_Artist_API_response = urllib2.urlopen('https://api.spotify.com/v1/artists/' + spotify_Artist_ID)
            json_Get_an_Artist_API_response = json.load(spotify_Get_an_Artist_API_response)
            spotify_Primary_Genre = json_Get_an_Artist_API_response['genres'][0]
            spotify_Secondary_Genre = json_Get_an_Artist_API_response['genres'][1]
            new_artist = Artists.objects.create(ArtistName=spotify_Artist_Name, SpotifyID=spotify_Artist_ID, PrimaryGenre=spotify_Primary_Genre, SecondaryGenre=spotify_Secondary_Genre)
            new_artist.save()
            matched_artist = Artists.objects.filter(SpotifyID=json_Search_response['albums']['items'][0]['id'])
        # get artist from matched_artist querySet
        # new_album = Album.objects.create(AlbumTitle=album_title, SpotifyAlbumID=json_Search_response['albums']['items'][0]['id'], ArtistName=artist.id, Favorite=0)
        # new_album.save()

    # Don't have spotify_Artist_ID (defined and use in if statement)
    # artistSet = Artists.objects.filter(SpotifyID=spotify_Artist_ID)
    # print artistSet
    # artist = artistSet.objects.get(AlbumTitle=album_title)
    # artist_name = artist.ArtistName
    # print artist.ArtistName

    # GET_ALBUM_REVIEW
    # Pitchfork Libary search() Feature Currently Broken
    # review = pitchfork.search(artist, album)
    review = 'Haven\'t decided what I\'m going to do here....' 
    album_title  = album_title.title()
    # TESTING SPOTIFY API
    

    # ECHONEST API
    # url2 = 'http://developer.echonest.com/api/v4/artist/news?api_key=JXWIZXVWFCDBT9DVG&id=spotify:artist:5l8VQNuIg0turYE1VtM9zV&format=json'
    # API_response = urllib2.urlopen(url)
    # json_response = json.load(API_response)

    return render(request, 'album_review.html', {'ALBUM': album_title, 'ARTIST': artist_name, 'REVIEW': review})

###################
#  HELPER FUNCTIONS
###################

def convert_to_query(album_title):
    queryTitle = ''
    for character in range(len(album_title)):
        if album_title[character] == ' ':
            queryTitle += '+'
        else:
            queryTitle += album_title[character]
    return queryTitle

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


    