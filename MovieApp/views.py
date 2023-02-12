from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from MovieApp.models import *
from MovieApp.serializers import *



# Create your views here.

@csrf_exempt
def movieApi(request,id=0):
    if request.method=='GET':
        movie = Movie.objects.all()
        movie_serializer = MovieSerializer(movie,many=True)
        return JsonResponse(movie_serializer.data,safe=False)
    
    elif request.method=='POST':
        movie_data = JSONParser().parse(request)
        movie_serializer = MovieSerializer(data=movie_data)
        if movie_serializer.is_valid():
            movie_serializer.save()
            movie = Movie.objects.get(MovieTitle=movie_data["MovieTitle"])
            for actors in movie_data["ActorLists"]:
                actor = Actor.objects.get(ActorName=actors)
                actor.ActorMovies += 1
                actor.save(update_fields=["ActorMovies"])
                actor.MovieLists.append(movie_data["MovieTitle"])
                actor.save(update_fields=["MovieLists"])
                MovieActor.objects.create(Movie=movie,Actor=actor)
            return JsonResponse("Added Successfully!",safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        movie_data = JSONParser().parse(request)
        movie = Movie.objects.get(MovieId=movie_data['MovieId'])
        movie_serializer = MovieSerializer(movie,data=movie_data)
        if movie_serializer.is_valid():
            for actors in movie.ActorLists:
                actor = Actor.objects.get(ActorName=actors)
                actor.ActorMovies -= 1
                actor.save(update_fields=["ActorMovies"])
                actor.MovieLists.remove(movie.MovieTitle)
                actor.save(update_fields=["MovieLists"])
            movie_serializer.save()
            for actors in movie_data["ActorLists"]:
                actor = Actor.objects.get(ActorName=actors)
                actor.ActorMovies += 1
                actor.save(update_fields=["ActorMovies"])
                actor.MovieLists.append(movie_data["MovieTitle"])
                actor.save(update_fields=["MovieLists"])
            return JsonResponse("Updated successfully!",safe=False)
        return JsonResponse("Failed to Update.",safe=False)
    
    elif request.method=='DELETE':
        movie = Movie.objects.get(MovieId=id)
        for actors in movie.ActorLists:
            actor = Actor.objects.get(ActorName=actors)
            actor.ActorMovies -= 1
            actor.save(update_fields=["ActorMovies"])
            actor.MovieLists.remove(movie.MovieTitle)
            actor.save(update_fields=["MovieLists"])
        movie.delete()
        return JsonResponse("Deleted Successfully!",safe=False)

@csrf_exempt  
def actorApi(request,id=0):
    if request.method=='GET':
        actor = Actor.objects.all()
        actor_serializer = ActorSerializer(actor,many=True)
        return JsonResponse(actor_serializer.data,safe=False)
    
    elif request.method=='POST':
        actor_data = JSONParser().parse(request)
        actor_serializer = ActorSerializer(data=actor_data)
        if actor_serializer.is_valid():
            actor_serializer.save()
            actor = Actor.objects.get(ActorName=actor_data["ActorName"])
            for movies in actor_data["MovieLists"]:
                movie = Movie.objects.get(MovieTitle=movies)
                movie.MovieActors += 1
                movie.save(update_fields=["MovieActors"])
                movie.ActorLists.append(actor_data["ActorName"])
                movie.save(update_fields=["ActorLists"])
                MovieActor.objects.create(Movie=movie,Actor=actor)
            return JsonResponse("Added Successfully!",safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        actor_data = JSONParser().parse(request)
        actor = Actor.objects.get(ActorId=actor_data['ActorId'])
        actor_serializer = ActorSerializer(actor,data=actor_data)
        if actor_serializer.is_valid():
            for movies in actor.MovieLists:
                movie = Movie.objects.get(MovieTitle=movies)
                movie.MovieActors -= 1
                movie.save(update_fields=["MovieActors"])
                movie.ActorLists.remove(actor.ActorName)
                movie.save(update_fields=["ActorLists"])
            actor_serializer.save()
            for movies in actor_data["MovieLists"]:
                movie = Movie.objects.get(MovieTitle=movies)
                movie.MovieActors += 1
                movie.save(update_fields=["MovieActors"])
                movie.ActorLists.append(actor_data["ActorName"])
                movie.save(update_fields=["ActorLists"])
            return JsonResponse("Updated successfully!",safe=False)
        return JsonResponse("Failed to Update.",safe=False)
    
    elif request.method=='DELETE':
        actor = Actor.objects.get(ActorId=id)
        for movies in actor.MovieLists:
            movie = Movie.objects.get(MovieTitle=movies)
            movie.MovieActors -= 1
            movie.save(update_fields=["MovieActors"])
            movie.ActorLists.remove(actor.ActorName)
            movie.save(update_fields=["ActorLists"])
        actor.delete()
        return JsonResponse("Deleted Successfully!",safe=False)

@csrf_exempt
def sortApi(request,id):
    if request.method=='GET':
        if id=="title":
            movie = Movie.objects.all().order_by('MovieTitle')
            movie_serializer = MovieSerializer(movie,many=True)
            return JsonResponse(movie_serializer.data,safe=False)
        elif id=="date":
            movie = Movie.objects.all().order_by('MovieReleaseDate')
            movie_serializer = MovieSerializer(movie,many=True)
            return JsonResponse(movie_serializer.data,safe=False)
        return JsonResponse("Sorting Unsuccessful",safe=False)