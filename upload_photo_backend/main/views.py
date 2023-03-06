from datetime import timedelta

from rest_framework import serializers
from django.utils import timezone
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from .serializers import ImageSerializer, BinaryImageSerializer
from .models import Image, BinaryImage


class ImageUploadView(CreateAPIView):
    serializer_class = ImageSerializer

    @staticmethod
    def validation_expiring_time(expiring_time):
        if not expiring_time:
            return None
        try:
            expiring_time = int(expiring_time)
            if 300 <= expiring_time <= 30000:
                return expiring_time
            else:
                raise serializers.ValidationError("Expiring time must be between 300 and 30000")
        except ValueError:
            raise serializers.ValidationError("Invalid expiring time")

    def perform_create(self, serializer):
        try:
            expiring_time = self.request.data.get("expiring_time")
        except:
            expiring_time = None

        expiring_time = self.validation_expiring_time(expiring_time)

        instance = serializer.save(user=self.request.user)

        if expiring_time and instance.user.type_account.binary:
            expiring_time = timedelta(seconds=expiring_time) + timezone.now()
            BinaryImage.objects.create(
                expired=expiring_time,
                image_binary=instance.photo.read(),
                image=instance
            )


class ListImageView(ListAPIView):
    model = Image
    serializer_class = ImageSerializer

    def get_queryset(self):
        queryset = None
        if self.request.user.is_authenticated:
            queryset = Image.objects.filter(user=self.request.user)
        return queryset


class BinaryImageGetView(RetrieveAPIView):
    queryset = BinaryImage.objects.all()
    serializer_class = BinaryImageSerializer

    def get_object(self):
        object_to_validate = super().get_object()
        if object_to_validate.expired > timezone.now():
            return object_to_validate
        else:
            raise Exception("Binary is expired")
