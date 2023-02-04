from rest_framework.serializers import ModelSerializer
from base.models import Room
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RoomSerialzer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
