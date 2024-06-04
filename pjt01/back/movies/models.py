from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    # genre_id = models.IntegerField()
    genre_name = models.CharField(max_length=100)

class Movie(models.Model) :
    pick_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='picked_movies')
    genres = models.ManyToManyField(Genre)
    
    title = models.CharField(max_length=250)
    tagline = models.TextField(blank=True, null=True)
    runtime = models.IntegerField()
    original_title = models.CharField(max_length=250)
    original_language = models.TextField()
    original_country = models.TextField()
    overview = models.TextField(blank=True)
    poster_path = models.TextField()
    backdrop_path = models.TextField() 
    popularity = models.FloatField()
    vote_average = models.FloatField()
    vote_count = models.FloatField()
    release_date = models.DateField()
    trailer = models.URLField(max_length=255, blank=True, null=True)
    director = models.TextField()
    actors = models.TextField()


class Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_reviews", blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews" )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    
    title = models.CharField(max_length=50)
    famous_line = models.TextField()
    content = models.TextField()
    watched_at = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    is_opened = models.BooleanField()
    rating = models.FloatField()
