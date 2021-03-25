from rest_framework import serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView, \
    DestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser

from movies.models import Movie, Genre


class MovieSerializer(serializers.ModelSerializer):
    visibility = serializers.BooleanField(required=True)
    genre = serializers.SlugRelatedField(slug_field="guid",
                                         queryset=Genre.objects.get_visible(), many=True)

    class Meta:
        model = Movie
        fields = (
            "guid", "title", "genre", "visibility", "movie_image",
            "video_image", "published_date", "country", "company",
            "description", "duration", "created_date",
            "modified_date",
            "creator")


class CreateMovieView(CreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        genres = serializer.validated_data.pop("genre")
        movie = Movie.objects.create(**serializer.validated_data,
                                                   creator=self.request.user)
        movie.genre.add(*genres)
        serializer.instance = movie


class UpdateMovieView(UpdateAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAdminUser,)
    queryset = Movie.objects.all()
    lookup_field = "guid"

    # def perform_update(self, serializer):


# class DetailGenreView(RetrieveAPIView):
#     serializer_class = GenreSerializer
#     permission_classes = (IsAdminUser,)
#     queryset = Genre.objects.all()
#     lookup_field = "guid"


class DeleteMovieView(DestroyAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAdminUser,)
    queryset = Movie.objects.all()
    lookup_field = "guid"

# class ListGenreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Genre
#         fields = ("guid", "title")
#
#
# class AdminListGenreView(ListAPIView):
#     permission_classes = (IsAdminUser,)
#     serializer_class = ListGenreSerializer
#
#     def get_queryset(self):
#         return Genre.objects.all()
#
#
# class ListGenreView(ListAPIView):
#     serializer_class = ListGenreSerializer
#
#     def get_queryset(self):
#         return Genre.objects.get_visible()
