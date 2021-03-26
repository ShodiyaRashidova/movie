from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView, \
    DestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser

from common.pagination import AdminPagination, Pagination
from movies.models import Movie, Genre


class MovieSerializer(serializers.ModelSerializer):
    visibility = serializers.BooleanField(required=True)
    genre = serializers.SlugRelatedField(slug_field="guid",
                                         queryset=Genre.objects.get_visible(),
                                         many=True)

    class Meta:
        model = Movie
        exclude = ("id",)


class CreateMovieView(CreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        serializer.instance = Movie.objects.create_with_genre(
            serializer.validated_data, self.request.user)


class UpdateMovieView(UpdateAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAdminUser,)
    queryset = Movie.objects.all()
    lookup_field = "guid"

    def perform_update(self, serializer):
        serializer.instance.update_with_genre(serializer.validated_data)


class AdminDetailMovieView(RetrieveAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAdminUser,)
    queryset = Movie.objects.all()
    lookup_field = "guid"


class DeleteMovieView(DestroyAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAdminUser,)
    queryset = Movie.objects.prefetch_related("genres")
    lookup_field = "guid"


class AdminListGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            "guid", "title", "movie_image", "published_date", "country",
            "rating",
            "duration", "age_limit", "producer", "company")


class MovieFilter(filters.FilterSet):
    genre = filters.CharFilter(
        field_name="genre__guid", lookup_expr="exact"
    )

    class Meta:
        model = Movie
        fields = ["genre"]


class AdminListMovieView(ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = AdminListGenreSerializer
    pagination_class = AdminPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter

    def get_queryset(self):
        return Movie.objects.all().order_by("-id")


class ListMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            "guid", "title", "movie_image", "rating", "age_limit", "duration")


class ListMovieView(ListAPIView):
    serializer_class = ListMovieSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter

    def get_queryset(self):
        return Movie.objects.get_visible()


class DetailMovieSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True, slug_field="title",
                                         read_only=True)

    class Meta:
        model = Movie
        exclude = (
        "id", "created_date", "modified_date", "creator", "visibility")


class DetailMovieView(RetrieveAPIView):
    serializer_class = DetailMovieSerializer
    queryset = Movie.objects.get_visible()
    lookup_field = "guid"
