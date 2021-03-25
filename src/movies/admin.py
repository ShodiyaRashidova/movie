from django.contrib import admin

from movies.models import Genre, Movie


class GenreAdmin(admin.ModelAdmin):
    model = Genre
    list_display = ("guid", "title", "creator", "created_date", "modified_date")


class MovieAdmin(admin.ModelAdmin):
    model = Movie
    list_display = (
        "guid", "title", "duration", "creator", "created_date", "modified_date")


admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
