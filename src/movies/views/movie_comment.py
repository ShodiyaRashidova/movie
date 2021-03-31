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


# class ListMovieCommentView(ListAPIView):
#     serializer_class = AdminListGenreSerializer
#     pagination_class = AdminPagination
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = MovieFilter
#
#     def get_queryset(self):
#         return MovieComment.objects.all()
