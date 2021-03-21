from rest_framework import serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView, \
    DestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser

from ..models import FAQ
from ..pagination import AdminPagination


class FAQSerializer(serializers.Serializer):
    guid = serializers.UUIDField(read_only=True)
    question = serializers.CharField()
    answer = serializers.CharField()
    visibility = serializers.BooleanField()
    creator = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)
    modified_date = serializers.DateTimeField(read_only=True)


class CreateFAQView(CreateAPIView):
    serializer_class = FAQSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        serializer.instance = FAQ.objects.create(
            **serializer.validated_data, creator=self.request.user)


class UpdateFAQView(UpdateAPIView):
    serializer_class = FAQSerializer
    permission_classes = (IsAdminUser,)
    queryset = FAQ.objects.all()
    lookup_field = "guid"

    def perform_update(self, serializer):
        serializer.instance.update(serializer.validated_data)


class DeleteFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ("guid",)


class DeleteFAQView(DestroyAPIView):
    http_method_names = ["delete"]
    queryset = FAQ.objects.all()
    serializer_class = DeleteFAQSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "guid"


class AdminDetailFAQView(RetrieveAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = FAQSerializer
    lookup_field = "guid"
    queryset = FAQ.objects.all()


class AdminListFAQView(ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = FAQSerializer
    pagination_class = AdminPagination

    def get_queryset(self):
        return FAQ.objects.all()


class ListFAQSerializer(serializers.Serializer):
    guid = serializers.UUIDField(read_only=True)
    question = serializers.CharField()
    answer = serializers.CharField()


class ListFAQView(ListAPIView):
    serializer_class = ListFAQSerializer

    def get_queryset(self):
        return FAQ.objects.get_visible()
