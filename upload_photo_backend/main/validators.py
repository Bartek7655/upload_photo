import os

from rest_framework import serializers


def validate_format_image(value):
    ext = os.path.splitext(value.name)[1]
    valid_extension = ['.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extension:
        raise serializers.ValidationError("Extension is incorrect")
