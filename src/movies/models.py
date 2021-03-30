import uuid

from django.conf import settings
from django.db import models

from common.models import BaseModel, BaseManager


class GenreManager(BaseManager):
    pass


class Genre(BaseModel):
    title = models.CharField(max_length=30)
    objects = GenreManager()

    def __str__(self):
        return f"{self.title}"


class MovieManager(BaseManager):

    def create_with_genre(self, data, user):
        genres = data.pop("genre")
        movie = Movie.objects.create(**data, creator=user)
        movie.genre.set(genres)
        return movie


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
    age_limit = models.PositiveIntegerField()
    rating = models.PositiveIntegerField()
    objects = MovieManager()

    def update_with_genre(self, data):
        genres = data.pop("genre")
        for field, value in data.items():
            setattr(self, field, value)
        self.save()
        self.genre.set(genres)

    def __str__(self):
        return f"{self.title}"


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

    def __str__(self):
        return f"{self.name}"


class MovieSchedule(BaseModel):
    movie = models.ForeignKey(Movie, related_name="schedules",
                              related_query_name="schedule",
                              on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, related_name="schedules",
                             related_query_name="schedule",
                             on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.movie}, {self.hall}, {self.start_time}"


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
    content = models.TextField(blank=True)
