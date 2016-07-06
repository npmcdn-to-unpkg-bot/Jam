from django import template
from time import gmtime, strftime
from django.shortcuts import get_object_or_404, render
from django.http import  Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from jam.models import Artists, Album
from jam.API_Config import *
import pitchfork
import urllib
try:
    import urllib.request as urllib2
except ImportError:
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

#####################
#               CACHE
#####################

features_cache = set()

########################
#  FEATURE WRAPPER CLASS
########################

class Feature:

    def __init__(self, name, title, review):
        self.artistName = name
        self.albumTitle = title
        self.featureReview = review

    def __unicode__(self):
        return self.artistName + " " + self.albumTitle + " " + self.featureReview

#######################
#    JAM VIEW FUNCTIONS
#######################

def lets_jam(request):
    # Home Page of JAM
    # Page to display Featured Favorite Albums
    featured_albums_list = list(Album.objects.filter(Favorite=1))

    if featured_albums_list != []:
        no_features = 0
        features = []
        for album in featured_albums_list:
            artist = Artists.objects.get(SpotifyID=album.ArtistID_id)
            feature = Feature(artist.ArtistName, album.AlbumTitle, "TESTING TESTING TESTING TESTINGTESTING TESTING TESTING TESTINGTESTING TESTING TESTING TESTINGTESTING TESTING TESTING TESTINGTESTING TESTING TESTING TESTING")
            features.append(feature)
    else:
        no_features = 1

    return render(request, 'features_home.html', {'no_features': no_features, 'featured_albums': features, 'article_header': "featured albums"})

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
    albumSet = Album.objects.filter(AlbumTitle__icontains=album_title)
    if not albumSet:
        # if empty: No Corresponding Album
        raise Http404  
    else: 
        album_title = "Doris"
        artist_name = "Earl Sweatshirt"
        review = "TESTING 1 2 3"; # Index and grab review.
        truth = 1
        return render(request, 'album_review.html', {'true': truth, 'albumTitle': album_title, 'artistName': artist_name, 'featureReview': review, 'article_header': "album review"})

    # get artist from matched_artist querySet
    new_album = Album.objects.create(AlbumTitle=album_title, SpotifyAlbumID=json_Search_response['albums']['items'][0]['id'], ArtistName=artist.id, Favorite=0)
    new_album.save()
    # else:
        # Get album from database // Index

    # GET_ALBUM_REVIEW
    review = 'where my user review will be' 
    album_title  = album_title.title()
    return render(request, 'album_review.html', {'albumTitle': album_title, 'artistName': artist_name, 'featureReview': review, 'article_header': "album review"})

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

#######################
# PITCHFORK API WRAPPER
#######################
def search(request, artist, album):
    review = pitchfork.search(url_argument_parse(artist), url_argument_parse(album))
    review_dictionary = {"artist": review.artist(), "album": review.album(), \
        "editorial": review.editorial(), "label": review.label(), "score": review.score()}
    return JsonResponse(review_dictionary)


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
    pic_url = urllib2.urlopen("https://farm2.staticflickr.com/1627/24943678040_d9637bdeee_c.jpg")
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

