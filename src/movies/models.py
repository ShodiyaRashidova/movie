import uuid

from django.conf import settings
from django.db import models

from common.models import BaseModel, BaseManager


class GenreManager(BaseManager):
    pass


class Genre(BaseModel):
    title = models.CharField(max_length=30)
    objects = GenreManager()


class MovieManager(BaseManager):
    pass


class Movie(BaseModel):
    genre = models.ManyToManyField(Genre, related_name="movies",
                                   related_query_name="movie")
    title = models.CharField(max_length=100)
    movie_image = models.URLField()
    video_image = models.URLField()
    video = models.URLField()
    published_date = models.DateField()
    country = models.CharField(max_length=255)
    producer = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.DurationField()
    age_limit = models.PositiveIntegerField(default=0)
    objects = MovieManager()


class MovieRating(models.Model):
    movie = models.ForeignKey(Movie, related_name="rating",
                              related_query_name="rate",
                              on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="rating1",
        related_query_name="rate1",
        editable=False
    )


class Hall(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        editable=False
    )


class MovieSchedule(BaseModel):
    movie = models.ForeignKey(Movie, related_name="schedules",
                              related_query_name="schedule",
                              on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, related_name="schedules",
                             related_query_name="schedule",
                             on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    price = models.FloatField()


class MovieComment(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey(Movie, related_name="comments",
                              related_query_name="comment",
                              on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment",
    )
    created_date = models.DateTimeField(auto_now_add=True)
