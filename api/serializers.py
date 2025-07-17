from django.contrib.auth import get_user_model
from rest_framework import serializers

from air import models
from air.models import AirlineUser


def generate_serializer(model, allowed_fields):
    meta_class = type("Meta", (), {
        "model": model,
        "fields": allowed_fields,
    })
    return type(
        f"{model.__name__}Serializer",
        (serializers.ModelSerializer,),
        {"Meta": meta_class},
    )


class MealSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    dietary = serializers.SerializerMethodField()

    class Meta:
        model = models.Meal
        fields = [
            "id",
            "name",
            "description",
            "price",
            "image",
            "stripe_price_id",
            "dietary",
        ]

    def get_image(self, obj):
        return obj.image_url

    def get_dietary(self, obj):
        return [option.name for option in obj.dietary_options.all()]


AirlineUserSerializer = generate_serializer(models.AirlineUser, ["id", "username", "first_name", "last_name", "role", "email", "is_active", "is_staff", "is_superuser", "last_login", "date_joined", "date_joined"])
BaggageSerializer = generate_serializer(models.Baggage, "__all__")
ComfortSerializer = generate_serializer(models.Comfort, "__all__")
AirplaneSerializer = generate_serializer(models.Airplane, "__all__")
FlightSerializer = generate_serializer(models.Flight, "__all__")
TicketSerializer = generate_serializer(models.Ticket, "__all__")
CheckInSerializer = generate_serializer(models.CheckIn, "__all__")
BoardingPassSerializer = generate_serializer(models.BoardingPass, "__all__")
DietaryOptionsSerializer = generate_serializer(models.DietaryOption, "__all__")


class CurrentUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    role = serializers.CharField()

    class Meta:
        model = AirlineUser
        fields = ["id", "name", "email", "role"]

    def get_name(self, obj):
        return obj.get_full_name()
