from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from .serializers import ImageSerializer
from .models import Image, BinaryImage


class ImageUploadView(CreateAPIView):
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        expiring_time = int(self.request.data.get('expiring_time', 300))
        instance = serializer.save(user=self.request.user)

        if expiring_time and instance.user.type_account.binary:
            BinaryImage.objects.create(
                expiring_time=expiring_time,
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
