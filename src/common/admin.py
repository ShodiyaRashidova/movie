from django.contrib import admin

from .models import News, FAQ, ImageStorage


class NewsAdmin(admin.ModelAdmin):
    model = News
    list_display = (
        "guid", "title", "visibility", "creator", "created_date",
        "modified_date")
    list_editable = ("visibility",)
    list_filter = ("visibility", "creator")
    search_fields = ("title",)


class FAQAdmin(admin.ModelAdmin):
    model = FAQ
    list_display = (
        "guid", "question", "answer", "visibility", "creator", "created_date",
        "modified_date")
    list_editable = ("visibility",)
    list_filter = ("visibility", "creator")
    search_fields = ("question", "answer")


class ImageStorageAdmin(admin.ModelAdmin):
    model = ImageStorage
    list_display = ("guid","image", "creator", "created_date", "modified_date")


admin.site.register(News, NewsAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(ImageStorage, ImageStorageAdmin)
