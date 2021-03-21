from django.core.validators import get_available_image_extensions
from rest_framework import serializers
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from ..models import ImageStorage


class UploadImageSerializer(serializers.ModelSerializer):
    guid = serializers.UUIDField(read_only=True)
    image = serializers.ImageField()

    class Meta:
        model = ImageStorage
        fields = ("guid", "image")


class UploadImageAPIView(CreateAPIView):
    http_method_names = ["post"]
    serializer_class = UploadImageSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)