from rest_framework import serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView, \
    DestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser

from ..models import News
from ..pagination import AdminPagination, Pagination


class NewsSerializer(serializers.Serializer):
    guid = serializers.UUIDField(read_only=True)
    thumbnail = serializers.CharField()
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    visibility = serializers.BooleanField()
    creator = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)
    modified_date = serializers.DateTimeField(read_only=True)


class CreateNewsView(CreateAPIView):
    serializer_class = NewsSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        serializer.instance = News.objects.create(
            **serializer.validated_data, creator=self.request.user)


class UpdateNewsView(UpdateAPIView):
    serializer_class = NewsSerializer
    permission_classes = (IsAdminUser,)
    queryset = News.objects.all()
    lookup_field = "guid"

    def perform_update(self, serializer):
        serializer.instance.update(serializer.validated_data)


class DeleteNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ("guid",)


class DeleteNewsView(DestroyAPIView):
    http_method_names = ["delete"]
    queryset = News.objects.all()
    serializer_class = DeleteNewsSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "guid"


class AdminDetailNewsView(RetrieveAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = NewsSerializer
    lookup_field = "guid"
    queryset = News.objects.all()


class AdminListNewsView(ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = NewsSerializer
    pagination_class = AdminPagination

    def get_queryset(self):
        return News.objects.all()



class ListNewsSerializer(serializers.Serializer):
    guid = serializers.UUIDField(read_only=True)
    thumbnail = serializers.CharField()
    title = serializers.CharField(max_length=255)


class DetailNewsSerializer(serializers.Serializer):
    guid = serializers.UUIDField(read_only=True)
    thumbnail = serializers.CharField()
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()


class ListNewsView(ListAPIView):
    serializer_class = ListNewsSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return News.objects.get_visible()


class DetailNewsView(RetrieveAPIView):
    serializer_class = DetailNewsSerializer
    lookup_field = "guid"
    queryset = News.objects.get_visible()
