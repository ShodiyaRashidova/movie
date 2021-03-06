from django.contrib import admin

from movies.models import Genre, Movie, MovieSchedule, Hall, Order


class GenreAdmin(admin.ModelAdmin):
    model = Genre
    list_display = ("guid", "title", "creator", "created_date", "modified_date")


class HallAdmin(admin.ModelAdmin):
    model = Hall
    list_display = (
        "guid", "name", "capacity", "creator", "created_date", "modified_date")


class MovieAdmin(admin.ModelAdmin):
    model = Movie
    list_display = (
        "guid", "title", "duration", "creator", "created_date", "modified_date")
    list_filter = ("genre",)


class MovieScheduleAdmin(admin.ModelAdmin):
    model = MovieSchedule
    list_display = (
        "guid", "movie", "hall", "price", "movie_date", "movie_time", "creator",
        "created_date", "modified_date")
    list_filter = ("movie__title", "hall__name")


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = (
        "guid", "schedule", "quantity", "user", "price", "paid", "created_date",
        "modified_date")


admin.site.register(Movie, MovieAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(MovieSchedule, MovieScheduleAdmin)
admin.site.register(Order, OrderAdmin)