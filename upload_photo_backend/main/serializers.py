
from rest_framework import serializers

from .models import Image, BinaryImage
from .validators import validate_format_image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        extra_kwargs = {
            "photo": {'validators': [validate_format_image, ]}
        }
        model = Image
        fields = ('photo', )


class BinaryImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = BinaryImage
        fields = ('image_binary', )
