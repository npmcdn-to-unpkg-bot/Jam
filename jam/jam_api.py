from rest_framework import mixins, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jam.models import Artists, Album
from jam.API_Config import *

###############################
#   JAM API FUNCTIONS & CLASSES
###############################

@api_view(['GET', ])
@permission_classes((AllowAny, ))
def artist_detail(request, pk):
    # pk = primary key = Artist.SpotifyID
    try:
        result = Artists.objects.get(SpotifyID = pk)
    except Artists.DoesNotExist: 
        # Don't like this, return a JSON with error message not 404 response
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ArtistSerializer(result)
        return Response(serializer.data)

class ArtistList(generics.ListCreateAPIView):
    querySet = Artists.objects.all()
    serializer_class = ArtistSerializer
    # generics pre-packaged functions: get(), create()

class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artists.objects.all()
    serializer_class = ArtistSerializer    
    # generics pre-packaged functions: get(), put(), destroy() 

class AlbumList(generics.ListCreateAPIView):
    querySet = Albums.objects.all()
    serializer_class = AlbumSerializer

class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer