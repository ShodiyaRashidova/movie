from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from movies.models import Order, MovieSchedule, Hall


class OrderSerializer(serializers.ModelSerializer):
    schedule = serializers.SlugRelatedField(slug_field="guid",
                                            queryset=MovieSchedule.objects.all())
    user = serializers.CharField(read_only=True)
    price = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = ("guid", "user", "schedule", "quantity", "price")

    def validate(self, attrs):
        schedule = attrs["schedule"]
        available = schedule.get_available()
        if attrs["quantity"] > available:
            raise ValidationError("Not enough tickets")
        attrs["price"] = attrs["quantity"] * schedule.price

        return attrs


class CreateOrderView(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.instance = Order.objects.create(
            **serializer.validated_data, user=self.request.user)


class MovieScheduleSerializer(serializers.Serializer):
    movie = serializers.SlugRelatedField(slug_field="title", read_only=True)
    hall = serializers.SlugRelatedField(slug_field="name", read_only=True)
    movie_date = serializers.DateField()
    movie_time = serializers.TimeField()
    price = serializers.FloatField()


class ListOrderSerializer(serializers.Serializer):
    guid = serializers.UUIDField()
    quantity = serializers.IntegerField()
    price = serializers.FloatField()
    schedule = MovieScheduleSerializer()
    created_date = serializers.DateTimeField()


class ListOrderView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListOrderSerializer

    def get_queryset(self):
        return Order.objects.select_related("schedule", "schedule__hall",
                                            "schedule__movie").filter(
            user=self.request.user)


class UserSerializer(serializers.Serializer):
    guid = serializers.URLField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    profile_image = serializers.URLField()


class AdminListOrderSerializer(serializers.Serializer):
    guid = serializers.UUIDField()
    quantity = serializers.IntegerField()
    price = serializers.FloatField()
    created_date = serializers.DateTimeField()
    user = UserSerializer()


class AdminListOrderView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AdminListOrderSerializer

    def get_queryset(self):
        return Order.objects.select_related("user").filter(
            schedule__guid=self.kwargs["guid"])
