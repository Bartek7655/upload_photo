import io

from celery import shared_task
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image as ImagePIL

from .models import BinaryImage, SizeImageUpload


@shared_task
def resize_image_async(image_id, photo_bytes, sizes):
    image = ImagePIL.open(photo_bytes)

    for size in sizes:
        # name, extension = photo.name.split('.')[0].split('_')[0], photo.name.split('.')[-1]
        name, extension = 'test', '.jpg'
        ready_name = name + '_' + str(size.height) + '.' + extension

        resized_image = image.resize((size.width, size.height))
        buffer = io.BytesIO()
        resized_image.save(
            buffer,
            format=extension
        )
        buffer.seek(0)
        ready_image = ContentFile(
            buffer.getvalue(),
            name=ready_name
        )

        SizeImageUpload.objects.create(
            photo=ready_image,
            image_id=image_id
        )


@shared_task
def delete_expired_binary_links():
    BinaryImage.objects.filter(expired__lte=timezone.now()).delete()
