#jam/API_Config.py

from rest_framework import serializers, viewsets
from jam.models import Artists

###################
# API CONFIGURATION
###################

# All API's are read-only at the moment

# Serializers define the API representation.
class ArtistSerializer(serializers.ModelSerializer):
    
    # Using standard Serializer 
    
    # ArtistName = serializers.CharField(read_only=True)
    # SpotifyID = serializers.CharField(read_only=True)
    # PrimaryGenre = serializers.CharField(read_only=True)
    # SecondaryGenre = serializers.CharField(read_only=True)

    # serializers.Model

    class Meta:
        model = Artists
        fields = ('ArtistName', 'SpotifyID', 'PrimaryGenre', 'SecondaryGenre')

    # Search and return an instance of the Artist Class, give the validated data
    # def find(self, instance, validated_data):
    #     instance.ArtistName = validated_data.get('ArtistName', instance.ArtistName)
    #     instance.SpotifyID = validated_data.get('SpotifyID', instance.SpotifyID)
    #     instance.PrimaryGenre = validated_data.get('PrimaryGenre', instance.PrimaryGenre)
    #     instance.SecondaryGenre = validated_data.get('SecondaryGenre', instance.SecondaryGenre)
    #     return instance

# ViewSets define the view behavior.
class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artists.objects.all()
    serializer_class = ArtistSerializer