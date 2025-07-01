from django.contrib.auth import get_user_model
from rest_framework import serializers

from air import models
from air.models import AirlineUser


def generate_serializer(model):
    meta_class = type('Meta', (), {'model': model, 'fields': '__all__'})
    return type(f"{model.__name__}Serializer", (serializers.ModelSerializer,), {'Meta': meta_class})

class MealSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    dietary = serializers.SerializerMethodField()

    class Meta:
        model = models.Meal
        fields = ["id", "name", "description", "price", "image", "stripe_price_id", "dietary"]

    def get_image(self, obj):
        return obj.image_url

    def get_dietary(self, obj):
        return [option.name for option in obj.dietary_options.all()]

AirlineUserSerializer = generate_serializer(models.AirlineUser)
BaggageSerializer = generate_serializer(models.Baggage)
ComfortSerializer = generate_serializer(models.Comfort)
AirplaneSerializer = generate_serializer(models.Airplane)
FlightSerializer = generate_serializer(models.Flight)
TicketSerializer = generate_serializer(models.Ticket)
CheckInSerializer = generate_serializer(models.CheckIn)
BoardingPassSerializer = generate_serializer(models.BoardingPass)

class CurrentUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = AirlineUser
        fields = ['id', 'name', 'email','role']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_role(self, obj):
        return obj.role