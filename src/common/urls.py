from django.urls import path, include

from common.views.faq import CreateFAQView, UpdateFAQView, DeleteFAQView, \
    AdminDetailFAQView, AdminListFAQView, ListFAQView
from common.views.news import CreateNewsView, UpdateNewsView, DeleteNewsView, \
    AdminDetailNewsView, AdminListNewsView, ListNewsView, DetailNewsView

admin_news_url = [
    path("", AdminListNewsView.as_view(), name="list"),
    path("<uuid:guid>/", AdminDetailNewsView.as_view(), name="detail"),
    path("create/", CreateNewsView.as_view(), name="create"),
    path("<uuid:guid>/update/", UpdateNewsView.as_view(), name="update"),
    path("<uuid:guid>/delete/", DeleteNewsView.as_view(), name="delete"),
]

client_news_url = [
    path("", ListNewsView.as_view(), name="list"),
    path("<uuid:guid>/", DetailNewsView.as_view(), name="detail"),
]

admin_faq_url = [
    path("", AdminListFAQView.as_view(), name="list"),
    path("<uuid:guid>/", AdminDetailFAQView.as_view(), name="detail"),
    path("create/", CreateFAQView.as_view(), name="create"),
    path("<uuid:guid>/update/", UpdateFAQView.as_view(), name="update"),
    path("<uuid:guid>/delete/", DeleteFAQView.as_view(), name="delete"),
]

client_faq_url = [
    path("", ListFAQView.as_view(), name="list"),
]
