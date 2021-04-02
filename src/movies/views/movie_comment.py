from django.db.models import F
from rest_framework import serializers
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from ..models import MovieComment, Movie


class MovieCommentSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field="guid",
                                         queryset=Movie.objects.get_visible())
    creator = serializers.CharField(read_only=True)

    class Meta:
        model = MovieComment
        fields = ("guid", "content", "movie", "creator")


class CreateMovieCommentView(CreateAPIView):
    serializer_class = MovieCommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.instance = MovieComment.objects.create(
            **serializer.validated_data, creator=self.request.user)


class ListMovieCommentSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    user_image = serializers.URLField(read_only=True)

    class Meta:
        model = MovieComment
        fields = (
            "guid", "content", "movie", "email", "first_name", "last_name",
            "user_image",
            "created_date")


class ListMovieCommentView(ListAPIView):
    serializer_class = ListMovieCommentSerializer

    def get_queryset(self):
        return MovieComment.objects.annotate(
            email=F("creator__email"),
            first_name=F("creator__first_name"),
            last_name=F("creator__last_name"),
            user_image=F("creator__profile_image")
        ).filter(movie__guid=self.kwargs["guid"])
