#jam/API_Config.py

from rest_framework import serializers, viewsets
from jam.models import Artists

###################
# API CONFIGURATION
###################

# Serializers define the API representation.
class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artists
        fields = ('ArtistName', 'SpotifyID', 'PrimaryGenre', 'SecondaryGenre')


# ViewSets define the view behavior.
class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artists.objects.all()
    serializer_class = ArtistSerializer