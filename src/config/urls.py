"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from common.urls import admin_news_url
from common.urls import client_news_url
from common.urls import admin_faq_url
from common.urls import client_faq_url
from common.views.image import UploadImageAPIView

admin_urls = [
    path("news/", include((admin_news_url, "news"))),
    path("faq/", include((admin_faq_url, "faq"))),
]
client_urls = [
    path("news/", include((client_news_url, "news"))),
    path("faq/", include((client_faq_url, "faq"))),
]

urlpatterns = [
    path("", include((client_urls, "client"))),
    path("admin/", include((admin_urls, "admin1"))),
    path("upload/", UploadImageAPIView.as_view(), name="upload"),
    path("accounts/", include("accounts.urls")),
    path('django-admin/', admin.site.urls),
]
