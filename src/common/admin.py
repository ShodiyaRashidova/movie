from django.contrib import admin

from common.models import News


class NewsAdmin(admin.ModelAdmin):
    model = News
    list_display = ("guid",)
admin.site.register(News, NewsAdmin)