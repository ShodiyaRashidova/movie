import os
import uuid

from django.conf import settings
from django.core.validators import validate_image_file_extension
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class BaseManager(models.Manager):
    def get_visible(self):
        return self.filter(visibility=True)


class BaseModel(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        editable=False
    )
    visibility = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def update(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()


def upload_directory_path(instance, filename):
    filename_without_extension, extension = os.path.splitext(filename.lower())
    timestamp = timezone.now().strftime("%Y-%m-%d.%H-%M-%S")
    filename = f"{slugify(filename_without_extension)}.{timestamp}{extension}"
    folder = "admin" if instance.creator.is_staff else "user"
    return f"image/{folder}/{filename}"


class ImageStorage(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
    )
    image = models.ImageField(
        upload_to=upload_directory_path,
        validators=[validate_image_file_extension],
    )

    class Meta:
        db_table = "media"
        verbose_name = "Image File"
        verbose_name_plural = "Image Files"

    def __str__(self):
        return self.image.name


class NewsManager(models.Manager):
    def get_visible(self):
        return self.filter(visibility=True)


class News(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    thumbnail = models.URLField(max_length=255)
    objects = NewsManager()

    class Meta:
        ordering = ("-created_date",)
        db_table = "news"
        verbose_name = "News"
        verbose_name_plural = "News"


class FAQManager(models.Manager):
    def get_visible(self):
        return self.filter(visibility=True)


class FAQ(BaseModel):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    objects = FAQManager()

    class Meta:
        ordering = ("-created_date",)
        db_table = "faq"
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
