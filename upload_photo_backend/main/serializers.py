
from rest_framework import serializers

from .models import Image


class UserSerializer(serializers.ModelSerializer):
    pass


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('photo', )
