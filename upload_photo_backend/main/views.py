from rest_framework.generics import CreateAPIView, ListAPIView

from .serializers import ImageSerializer
from .models import Image


class ImageUploadView(CreateAPIView):
    serializer_class = ImageSerializer


class ListImageView(ListAPIView):
    model = Image
    serializer_class = ImageSerializer

    def get_queryset(self):
        queryset = None
        if self.request.user.is_authenticated:
            queryset = Image.objects.filter(user=self.request.user)
        return queryset

