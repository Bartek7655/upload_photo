from rest_framework.generics import CreateAPIView

from .serializers import ImageSerializer


class ImageUploadView(CreateAPIView):
    serializer_class = ImageSerializer
