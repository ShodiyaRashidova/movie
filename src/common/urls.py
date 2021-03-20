from django.urls import path, include

from common.views.news import CreateNewsView, UpdateNewsView, DeleteNewsView, \
    AdminDetailNewsView, AdminListNewsView

admin_news__url = [
    path("", AdminListNewsView.as_view(), name="list"),
    path("<uuid:guid>/", AdminDetailNewsView.as_view(), name="detail"),
    # path("news/", include(news_url)),
    path("create/", CreateNewsView.as_view(), name="create"),
    path("<uuid:guid>/update/", UpdateNewsView.as_view(), name="update"),
    path("<uuid:guid>/delete/", DeleteNewsView.as_view(), name="delete"),
]

client_url = [

]
