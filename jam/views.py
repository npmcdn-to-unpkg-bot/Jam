from django import template
from time import gmtime, strftime
from django.shortcuts import get_object_or_404, render
from django.http import  Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from jam.models import Artists, Album
from jam.API_Config import *
# from django.core.mail import send_mail
import urllib
import urllib2
import json

#####################
#  3RD PARTY API KEYS
#####################

spotify_api_key = '509df3f3d7584069a23c2db440960b20'
spotify_api_secret = 'e3826548f35d4ecb88c4eb8032ada051'
OAuth_token = 'BQDbMT3TcgCddi2y7_NehZU54TGQBk0MXbgO9izP5WrCeO40WqLdL98j88zeQwrMIBGj9'

echonest_api_key = 'JXWIZXVWFCDBT9DVG'
echonest_consumer_key = 'd3755c57dc73a9132325cd5bac8d4556'
echonest_shared_secret = '1b5YciWYSia7H0EMMM8rLw'

#######################
#    JAM VIEW FUNCTIONS
#######################

def lets_jam(request):
    # Home Page of JAM
    # Page to display Featured Favorite Albums
    all_artist = Artists.objects.all()
    featured_albums = list()
    no_features = 0
    for artist in all_artist:
        if len(Album.objects.filter(ArtistID=artist.artistID())) != 0:
            featured_albums.append(Album.objects.filter(ArtistID=artist.artistID()))
        else:
            # If no albums // Display Message
            no_features = 1
    # GET ALBUM COVERS

    test = 'anything in return'

    return render(request, 'lets_jam.html', {'no_features': no_features, 'featured_albums': featured_albums, 'test': test})

def lets_jam_recommend(request):
    # Recommendation Page
    if (request.method == 'GET'):
        return render(request, 'lets_jam_recommend.html', {'message': '', 'source': ""})
    else:
        try:

            recommened_item = request.POST['recommened_item']
            json_Search_response_artist, json_Search_response_album = spotify_gen_search(recommened_item)

            if (json_Search_response_album['albums']['items'] != [ ]):
                # Match
                message = "You've Successfully Recommmended: " + recommened_item.title() + "."
                # send_mail('New Jam Recommendation', 'Username: ' + "" + " recommendeds " + recommened_item.title(), 'evralcar@gmail.com', ['evralcar@gmail.com'], fail_silently=False)
                if (Album.objects.filter(AlbumTitle=recommened_item)):
                    # Matching Album
                    source = json_Search_response_album['albums']['items'][0]['images'][1]['url']
                    return render(request, "lets_jam_recommend.html", {'message': message, 'source': source})
                elif(json_Search_response_artist['artists']['items'] != [ ]):
                    # change sourse to get artist picture, not an album picture
                    source = json_Search_response_artist['artists']['items'][0]['images'][1]['url']
                    return render(request, "lets_jam_recommend.html", {'message': "We Have a Match!", 'source': source})
                else:
                    message = "Hey, what do you know, someone has already suggested " + recommened_item.title() + ". \n Probably because you've got good taste in Music!"
                    return render(request, "lets_jam_recommend.html", {'message': message, 'source': source})
            else:
                raise ValueError
        except ValueError:
            # we couldn't find your recommendation, display error message
            return render(request, 'lets_jam_recommend.html', {'message': 'We couldn\'t find that Album', 'source': ""})

def lets_jam_review(request, album_title):
    album_title = url_argument_parse(album_title)
    albumSet = Album.objects.filter(AlbumTitle=album_title)
    if not albumSet:
        # if empty: No Corresponding Album
        raise Http404  
    else: 
        # we have the album
        artist_name = "fix this";
        review = "fix this too"; # Index and grab review.
        return render(request, 'album_review.html', {'ALBUM': album_title, 'ARTIST': artist_name, 'REVIEW': review})

    # get artist from matched_artist querySet
    new_album = Album.objects.create(AlbumTitle=album_title, SpotifyAlbumID=json_Search_response['albums']['items'][0]['id'], ArtistName=artist.id, Favorite=0)
    new_album.save()
    # else:
        # Get album from database // Index

    # GET_ALBUM_REVIEW
    review = 'where my user review will be' 
    album_title  = album_title.title()

    return render(request, 'album_review.html', {'ALBUM': album_title, 'ARTIST': artist_name, 'REVIEW': review})

#####################
#   JAM API FUNCTIONS
#####################

def artist_detail(request, pk):
    # pk = primary key = Artist.SpotifyID
    try:
        result = Artists.objects.get(SpotifyID = pk)
    except Artists.DoesNotExist: 
        # Don't like this, return a JSON with error message not 404 response
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArtistSerializer(result)
        return JsonResponse(serializer.data)

###################
#   ADMIN FUNCTIONS
###################

def add_artist(request, artist_query):
    artist_query = url_argument_parse(artist_query)
    json_Search_response_artist, json_Search_response_album = spotify_gen_search(artist_query)

    spotify_Artist_ID = json_Search_response_artist['artists']['items'][0]['id']
    spotify_Artist_Name = json_Search_response_artist['artists']['items'][0]['name']

    if (json_Search_response_artist['artists']['items'][0]['genres'] != [ ]):
            spotify_Primary_Genre = json_Search_response_artist['artists']['items'][0]['genres'][0]
            try: 
                spotify_Secondary_Genre = json_Search_response_artist['artists']['items'][0]['genres'][1]
            except IndexError:
                spotify_Secondary_Genre = 'undefined'
    else:
        spotify_Primary_Genre = 'undefined'
        spotify_Secondary_Genre = 'undefined'

    new_artist = Artists.objects.create(ArtistName=spotify_Artist_Name, SpotifyID=spotify_Artist_ID, PrimaryGenre=spotify_Primary_Genre, SecondaryGenre=spotify_Secondary_Genre)
    new_artist.save()

    # temp success page redirect
    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    page_title = "Evan"
    pic_url = urllib.urlopen("https://farm2.staticflickr.com/1627/24943678040_d9637bdeee_c.jpg")
    return render(request, 'time.html', {'current_time': now, 'page_title': page_title})


def add_album(request, album_query):
    album_query = url_argument_parse(album_query)
    json_Search_response_artist, json_Search_response_album = spotify_gen_search(album_query)

    spotify_Album_ID = json_Search_response_album['albums']['items'][0]['id']
    spotify_Album_Name = json_Search_response_album['albums']['items'][0]['name']

    json_Search_response_album = spotify_album_search(spotify_Album_ID)
    spotify_Artist_ID = json_Search_response_album["artists"][0]["id"]
    spotify_Artist_Name = json_Search_response_album["artists"][0]["name"]

    artist = Artists.objects.filter(SpotifyID=spotify_Artist_ID)
    artist = list(artist[:1])

    new_album = Album.objects.create(AlbumTitle=spotify_Album_Name, SpotifyAlbumID=spotify_Album_ID, ArtistID=artist[0])
    new_album.save()


    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    page_title = "Successfully added " + spotify_Album_Name
    return render(request, 'time.html', {'current_time': now, 'page_title': page_title})

###################
#  HELPER FUNCTIONS
###################

def spotify_gen_search(recommened_item):
    spotify_Search_response_album = urllib2.urlopen('https://api.spotify.com/v1/search?q=' + convert_to_query(recommened_item) + '&type=album&market=US')
    json_Search_response_album = json.load(spotify_Search_response_album)
    spotify_Search_response_artist = urllib2.urlopen('https://api.spotify.com/v1/search?q=' + convert_to_query(recommened_item) + '&type=artist&market=US')
    json_Search_response_artist = json.load(spotify_Search_response_artist)
    return json_Search_response_artist, json_Search_response_album

def spotify_album_search(album_id):
    api_url = "https://api.spotify.com/v1/albums/" + album_id + "?market=US"
    json_Search_response_album = json.load(urllib2.urlopen(api_url))
    return json_Search_response_album


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

