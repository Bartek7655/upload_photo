
from rest_framework import serializers

from .models import Image


class UserSerializer(serializers.ModelSerializer):
    pass


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('photo', )

    # def create(self, validated_data):
    #     image = validated_data.get('image')
    #     original_image = ImagePIL.open(image)
    #
    #     image_list = []
    #
    #     # Save original image
    #     image_object = Image(image=image)
    #     image_object.save()
    #     image_list.append(image_object)
    #
    #     # Save resized image
    #     resized_image = original_image.resize((100, 100))
    #     buffer = io.BytesIO()
    #     resized_image.save(buffer, format="JPEG")
    #     buffer.seek(0)
    #     ready_image = ContentFile(buffer.read(), name=image.name)
    #     image_object = Image(image=ready_image)
    #     image_object.save()
    #     image_list.append(image_object)
    #
    #     return image
