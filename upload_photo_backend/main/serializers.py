
from rest_framework import serializers

from .models import Image, BinaryImage


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('photo', )


class BinaryImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = BinaryImage
        fields = ('image_binary', )
