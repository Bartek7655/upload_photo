from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from .serializers import ImageSerializer
from .models import Image, BinaryImage


class ImageUploadView(CreateAPIView):
    serializer_class = ImageSerializer

    def get_expiring_time(self):
        try:
            expiring_time = int(self.request.data.get('expiring_time'))
            if 300 <= expiring_time <= 30000:
                return expiring_time
            else:
                raise ValueError('Expiring time value is wrong.')
        except (TypeError, ValueError):
            raise ValueError('Expiring time value is wrong.')

    def perform_create(self, serializer):
        try:
            expiring_time = self.get_expiring_time()
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save(user=self.request.user)

        if expiring_time and instance.user.type_account.binary:
            expiring_time = timedelta(seconds=expiring_time) + timezone.now()
            BinaryImage.objects.create(
                expired=expiring_time,
                image_binary=instance.photo.read(),
                image=instance
            )

        # return Response({'success': True}, status=status.HTTP_201_CREATED)

# class ImageUploadView(CreateAPIView):
#     serializer_class = ImageSerializer
#
#     def get_expiring_time(self):
#         try:
#             expiring_time = int(self.request.data.get('expiring_time'))
#             print('expiring_time in view', expiring_time)
#             if 300 <= expiring_time <= 30000:
#                 return expiring_time
#             else:
#                 pass
#                 # print('teeeeeestujemy')
#                 # return HttpResponseBadRequest(JsonResponse({
#                 #     "error": "Expiring time value is wrong."
#                 # }))
#         except:
#             return None
#
#     def perform_create(self, serializer):
#         expiring_time = self.get_expiring_time()
#         instance = serializer.save(user=self.request.user)
#
#         if expiring_time and instance.user.type_account.binary:
#             expiring_time = timedelta(seconds=expiring_time) + timezone.now()
#             BinaryImage.objects.create(
#                 expired=expiring_time,
#                 image_binary=instance.photo.read(),
#                 image=instance
#             )
#
#         return Response(
#             {'error': 'Expiring times value is wrong'},
#             status=status.HTTP_400_BAD_REQUEST
#         )
#

class ListImageView(ListAPIView):
    model = Image
    serializer_class = ImageSerializer

    def get_queryset(self):
        queryset = None
        if self.request.user.is_authenticated:
            queryset = Image.objects.filter(user=self.request.user)
        return queryset
