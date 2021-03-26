from django.urls import path, include

from movies.views.genre import CreateGenreView, UpdateGenreView, \
    DetailGenreView, DeleteGenreView, AdminListGenreView, ListGenreView
from movies.views.hall import CreateHallView, UpdateHallView, DetailHallView, \
    DeleteHallView, AdminListHallView
from movies.views.movie import CreateMovieView, UpdateMovieView, \
    DeleteMovieView, DetailMovieView, AdminListMovieView, ListMovieView, \
    AdminDetailMovieView

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

admin_url = [
    path("genre/", include((admin_genre_url, "genre"))),
    path("hall/", include((admin_hall_url, "hall"))),
    path("movie/", include((admin_movie_url, "movie"))),
]

client_url = [
    path("genre/", ListGenreView.as_view(), name="genre_list"),
    path("movie/", ListMovieView.as_view(), name="movie_list"),
    path("movie/<uuid:guid>/", DetailMovieView.as_view(), name="movie_detail"),

]
