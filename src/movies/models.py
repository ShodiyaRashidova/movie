import uuid
from datetime import date

from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models
from django.db.models import F, Sum, Case, When
from django.db.models.functions import Coalesce

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

    def get_with_genre_visible(self):
        return self.prefetch_related("genre").filter(visibility=True).order_by(
            '-id')


class Movie(BaseModel):
    class MovieType(models.TextChoices):
        PLAY_NOW = "PLAY_NOW"
        WATCH_ONLINE = "WATCH_ONLINE"
        UPCOMING = "UPCOMING"

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
    rating = models.FloatField()
    movie_type = models.CharField(choices=MovieType.choices, max_length=15)
    movie_url = models.URLField(null=True)
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


class MovieScheduleManager(models.Manager):
    def get_dates(self, movie_guid):
        result = self.values("movie").annotate(
            movie_dates=ArrayAgg("movie_date", ordering="movie_date",
                                 distinct=True)
        ).values("movie_dates").filter(movie__guid=movie_guid,
                                       movie_date__gte=date.today())
        if result:
            return result[0]

    def get_times(self, movie_guid, movie_date):
        return self.annotate(hall_name=F("hall__name"),
                             available=Sum("hall__capacity", distinct=True) - Coalesce(Sum(
                                 "order__quantity"
                             ), 0)
                             ).filter(
            movie__guid=movie_guid,
            movie_date=movie_date).order_by(
            "movie_time")

    def get_with_hall_name(self):
        return self.annotate(hall_name=F("hall__name"),
                             available=Sum("hall__capacity", distinct=True) - Coalesce(Sum(
                                 "order__quantity"
                             ), 0))


class MovieSchedule(BaseModel):
    movie = models.ForeignKey(Movie, related_name="schedules",
                              related_query_name="schedule",
                              on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, related_name="schedules",
                             related_query_name="schedule",
                             on_delete=models.CASCADE)
    movie_date = models.DateField()
    movie_time = models.TimeField()
    price = models.FloatField()
    objects = MovieScheduleManager()

    def __str__(self):
        return f"{self.movie}, {self.hall}, {self.movie_date}, {self.movie_time}"

    def get_available(self):
        result = self.hall.capacity - self.orders.aggregate(
            booked=Coalesce(Sum("quantity"), 0)).get("booked")
        print(result)
        return result


class MovieComment(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey(Movie, related_name="comments",
                              related_query_name="comment",
                              on_delete=models.CASCADE)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment",
    )
    created_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()


class Order(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    schedule = models.ForeignKey(MovieSchedule, related_name="orders",
                                 related_query_name="order",
                                 on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="orders",
    )
    price = models.FloatField()
    paid = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
