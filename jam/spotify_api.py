import json
import urllib

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

####################
#  SPOTIFY FUNCTIONS
####################

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

###################
#  HELPER FUNCTIONS
###################

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