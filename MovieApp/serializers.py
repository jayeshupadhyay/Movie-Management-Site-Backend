from rest_framework import serializers
from MovieApp.models import *


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('MovieId','MovieTitle',
                  'MovieDescription','MovieReleaseDate',
                  'MovieUpvotes','MovieDownvotes','MovieActors','ActorLists')
        

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('ActorId','ActorName','ActorDOB','ActorMovies','MovieLists')

