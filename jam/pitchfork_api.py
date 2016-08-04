from django.http import JsonResponse
import pitchfork
import urllib

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

#######################
# PITCHFORK API WRAPPER
#######################
def search(request, artist, album):
    review = pitchfork.search(url_argument_parse(artist), url_argument_parse(album))
    review_dictionary = {"artist": review.artist(), "album": review.album(), \
        "editorial": review.editorial(), "label": review.label(), "score": review.score()}
    return JsonResponse(review_dictionary)


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