from rest_framework import serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView, \
    DestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser

from movies.models import Hall


class HallSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)
    modified_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Hall
        fields = ("guid", "name", "capacity", "creator", "created_date",
                  "modified_date")


class CreateHallView(CreateAPIView):
    serializer_class = HallSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        serializer.instance = Hall.objects.create(**serializer.validated_data,
                                                   creator=self.request.user)


class UpdateHallView(UpdateAPIView):
    serializer_class = HallSerializer
    permission_classes = (IsAdminUser,)
    queryset = Hall.objects.all()
    lookup_field = "guid"


class DetailHallView(RetrieveAPIView):
    serializer_class = HallSerializer
    permission_classes = (IsAdminUser,)
    queryset = Hall.objects.all()
    lookup_field = "guid"


class DeleteHallView(DestroyAPIView):
    serializer_class = HallSerializer
    permission_classes = (IsAdminUser,)
    queryset = Hall.objects.all()
    lookup_field = "guid"


class ListHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ("guid", "name")


class AdminListHallView(ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = ListHallSerializer

    def get_queryset(self):
        return Hall.objects.all()


