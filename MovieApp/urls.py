from django.urls import re_path,path
from MovieApp import views


urlpatterns=[
    path('movie/',views.movieApi),
    path('movie/sort/<id>',views.sortApi),
    path('actor/',views.actorApi),
    path('actor/<id>',views.actorApi)
]