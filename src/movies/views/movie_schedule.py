from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView, \
    DestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser

from common.pagination import AdminPagination
from ..models import MovieSchedule, Movie, Hall


class MovieScheduleSerializer(serializers.ModelSerializer):
    visibility = serializers.BooleanField(required=True)
    movie = serializers.SlugRelatedField(slug_field="guid",
                                         queryset=Movie.objects.get_visible())
    hall = serializers.SlugRelatedField(slug_field="guid",
                                        queryset=Hall.objects.all())
    creator = serializers.SlugRelatedField(slug_field="email", read_only=True)

    class Meta:
        model = MovieSchedule
        exclude = ("id",)


class CreateMovieScheduleView(CreateAPIView):
    serializer_class = MovieScheduleSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        serializer.instance = MovieSchedule.objects.create(
            **serializer.validated_data, creator=self.request.user)


class UpdateMovieScheduleView(UpdateAPIView):
    serializer_class = MovieScheduleSerializer
    permission_classes = (IsAdminUser,)
    queryset = MovieSchedule.objects.all()
    lookup_field = "guid"

    def perform_update(self, serializer):
        serializer.instance.update(serializer.validated_data)


class AdminDetailMovieScheduleView(RetrieveAPIView):
    serializer_class = MovieScheduleSerializer
    permission_classes = (IsAdminUser,)
    queryset = MovieSchedule.objects.all()
    lookup_field = "guid"


class DeleteMovieScheduleView(DestroyAPIView):
    serializer_class = MovieScheduleSerializer
    permission_classes = (IsAdminUser,)
    queryset = MovieSchedule.objects.all()
    lookup_field = "guid"


class AdminListMovieScheduleSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField()
    hall_name = serializers.CharField()

    class Meta:
        model = MovieSchedule
        fields = (
            "guid", "movie_title", "hall_name", "price", "movie_date",
            "movie_time")


class MovieScheduleFilter(filters.FilterSet):
    movie = filters.CharFilter(field_name="movie__guid", lookup_expr="exact")
    hall = filters.CharFilter(field_name="hall__guid", lookup_expr="exact")

    class Meta:
        model = MovieSchedule
        fields = ["movie", "hall"]


class AdminListMovieScheduleView(ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = AdminListMovieScheduleSerializer
    pagination_class = AdminPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieScheduleFilter

    def get_queryset(self):
        return MovieSchedule.objects.annotate(movie_title=F("movie__title"),
                                              hall_name=F(
                                                  "hall__name")).order_by("-id")


class ListMovieScheduleSerializer(serializers.ModelSerializer):
    hall_name = serializers.CharField()
    available = serializers.IntegerField()

    class Meta:
        model = MovieSchedule
        fields = ("guid", "hall_name", "price", "movie_time", "available")


class ListMovieScheduleView(ListAPIView):
    serializer_class = ListMovieScheduleSerializer

    def get_queryset(self):
        return MovieSchedule.objects.get_times(self.kwargs["guid"],
                                               self.kwargs["date"])


class ListMovieScheduleDateSerializer(serializers.Serializer):
    movie_dates = serializers.ListField()


class ListMovieScheduleDateView(RetrieveAPIView):
    serializer_class = ListMovieScheduleDateSerializer

    def get_object(self):
        return MovieSchedule.objects.get_dates(self.kwargs["guid"])


class DetailMovieScheduleSerializer(serializers.ModelSerializer):
    hall_name = serializers.CharField()

    class Meta:
        model = MovieSchedule
        fields = ("guid", "hall_name", "price", "movie_time")


class DetailMovieScheduleView(RetrieveAPIView):
    serializer_class = ListMovieScheduleSerializer
    lookup_field = "guid"

    def get_queryset(self):
        return MovieSchedule.objects.get_with_hall_name()
