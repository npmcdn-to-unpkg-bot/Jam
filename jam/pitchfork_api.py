from django.http import JsonResponse
from jam.spotify_api import url_argument_parse
import pitchfork
import re
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
        "editorial": repair_editorial(review.editorial()), "label": review.label(), "score": review.score()}
    return JsonResponse(review_dictionary)

def repair_editorial(editorial):
    print(editorial)
    regex = re.compile(r'.[A-Z]')
    repaired_editorial = ""
    for token in editorial.split():
        if regex.search(token) is not None:
            repaired_editorial += token.replace(".", ".\n ")
            repaired_editorial += " "
        else:
            repaired_editorial += token
            repaired_editorial += " "
    print(repaired_editorial)
    return repaired_editorial