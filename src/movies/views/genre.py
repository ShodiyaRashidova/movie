from rest_framework import serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView, \
    DestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser

from ..models import Genre


class GenreSerializer(serializers.ModelSerializer):
    visibility = serializers.BooleanField(required=True)
    creator = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)
    modified_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Genre
        fields = ("guid", "title", "visibility", "creator", "created_date",
                  "modified_date")


class CreateGenreView(CreateAPIView):
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        serializer.instance = Genre.objects.create(**serializer.validated_data,
                                                   creator=self.request.user)


class UpdateGenreView(UpdateAPIView):
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUser,)
    queryset = Genre.objects.all()
    lookup_field = "guid"


class DetailGenreView(RetrieveAPIView):
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUser,)
    queryset = Genre.objects.all()
    lookup_field = "guid"


class DeleteGenreView(DestroyAPIView):
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUser,)
    queryset = Genre.objects.all()
    lookup_field = "guid"


class ListGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("guid", "title")


class AdminListGenreView(ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = ListGenreSerializer

    def get_queryset(self):
        return Genre.objects.all()


class ListGenreView(ListAPIView):
    serializer_class = ListGenreSerializer

    def get_queryset(self):
        return Genre.objects.get_visible()


# class MovieSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = (
#             "guid", "title", "genre", "visibility", "movie_image",
#             "video_image", "published_date", "country", "company",
#             "description", "duration", "created_date",
#             "modified_date",
#             "creator")
