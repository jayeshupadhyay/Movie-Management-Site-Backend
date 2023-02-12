from django.db import models

# Create your models here.

class Movie(models.Model):
    MovieId = models.AutoField(primary_key=True)
    MovieTitle = models.CharField(max_length=100)
    MovieDescription = models.CharField(max_length=1000)
    MovieReleaseDate = models.DateField(default="2023-01-01")
    MovieUpvotes = models.IntegerField()
    MovieDownvotes = models.IntegerField()
    MovieActors = models.IntegerField(default="0")
    ActorLists = models.JSONField(default=list,blank=True)

    def __str__(self):
        return self.MovieTitle

class Actor(models.Model):
    ActorId = models.AutoField(primary_key=True)
    ActorName = models.CharField(max_length=100)
    ActorDOB = models.DateField(default="2023-01-01")
    ActorMovies = models.IntegerField(default="0")
    MovieLists = models.JSONField(default=list,blank=True)

    def __str__(self):
        return self.ActorName

class MovieActor(models.Model):
    Movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    Actor = models.ForeignKey(Actor,on_delete=models.CASCADE)
