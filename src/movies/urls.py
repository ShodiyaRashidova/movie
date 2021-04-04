from datetime import datetime

from django.urls import path, include, re_path, register_converter

from movies.views.genre import CreateGenreView, UpdateGenreView, \
    DetailGenreView, DeleteGenreView, AdminListGenreView, ListGenreView
from movies.views.hall import CreateHallView, UpdateHallView, DetailHallView, \
    DeleteHallView, AdminListHallView
from movies.views.movie import CreateMovieView, UpdateMovieView, \
    DeleteMovieView, DetailMovieView, AdminListMovieView, ListMovieView, \
    AdminDetailMovieView
from movies.views.movie_comment import CreateMovieCommentView, \
    ListMovieCommentView
from movies.views.movie_schedule import CreateMovieScheduleView, \
    UpdateMovieScheduleView, AdminDetailMovieScheduleView, \
    DeleteMovieScheduleView, AdminListMovieScheduleView, ListMovieScheduleView, \
    ListMovieScheduleDateView, DetailMovieScheduleView
from movies.views.order import CreateOrderView, ListOrderView, \
    AdminListOrderView

admin_genre_url = [
    path("", AdminListGenreView.as_view(), name="list"),
    path("create/", CreateGenreView.as_view(), name="create"),
    path("<uuid:guid>/update/", UpdateGenreView.as_view(), name="update"),
    path("<uuid:guid>/", DetailGenreView.as_view(), name="detail"),
    path("<uuid:guid>/delete/", DeleteGenreView.as_view(), name="delete"),

]
admin_hall_url = [
    path("", AdminListHallView.as_view(), name="list"),
    path("create/", CreateHallView.as_view(), name="create"),
    path("<uuid:guid>/update/", UpdateHallView.as_view(), name="update"),
    path("<uuid:guid>/", DetailHallView.as_view(), name="detail"),
    path("<uuid:guid>/delete/", DeleteHallView.as_view(), name="delete"),
]

admin_movie_url = [
    path("", AdminListMovieView.as_view(), name="list"),
    path("create/", CreateMovieView.as_view(), name="create"),
    path("<uuid:guid>/update/", UpdateMovieView.as_view(), name="update"),
    path("<uuid:guid>/", AdminDetailMovieView.as_view(), name="detail"),
    path("<uuid:guid>/delete/", DeleteMovieView.as_view(), name="delete"),
]

admin_movie_schedule_url = [

    path("", AdminListMovieScheduleView.as_view(), name="list"),
    path("create/", CreateMovieScheduleView.as_view(), name="create"),
    path("<uuid:guid>/update/", UpdateMovieScheduleView.as_view(),
         name="update"),
    path("<uuid:guid>/", AdminDetailMovieScheduleView.as_view(), name="detail"),
    path("<uuid:guid>/delete/", DeleteMovieScheduleView.as_view(),
         name="delete"),

]

admin_url = [
    path("genre/", include((admin_genre_url, "genre"))),
    path("hall/", include((admin_hall_url, "hall"))),
    path("movie/", include((admin_movie_url, "movie"))),
    path("movie-schedule/",
         include((admin_movie_schedule_url, "movie_schedule"))),
    path("order/movie-schedule/<uuid:guid>/", AdminListOrderView.as_view(),
         name="order"),

]


class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value


register_converter(DateConverter, 'date')

client_url = [
    path("genre/", ListGenreView.as_view(), name="genre_list"),
    path("movie/", ListMovieView.as_view(), name="movie_list"),
    path("movie/<uuid:guid>/", DetailMovieView.as_view(), name="movie_detail"),
    path("movie-comment/create/", CreateMovieCommentView.as_view(),
         name="movie_comment"),
    path("movie-comment/<uuid:guid>/", ListMovieCommentView.as_view(),
         name="movie_comment_list"),

    path("movie-schedule/<uuid:guid>/",
         DetailMovieScheduleView.as_view(),
         name="movie_schedule"),

    path("movie-schedule/<uuid:guid>/dates/",
         ListMovieScheduleDateView.as_view(),
         name="movie_schedule_date"),
    path("movie-schedule/<uuid:guid>/times/<date:date>/",
         ListMovieScheduleView.as_view(),
         name="movie_schedule_time"),
    path("order/create/", CreateOrderView.as_view(),
         name="order_create"),
    path("order/", ListOrderView.as_view(),
         name="order_list"),

]
