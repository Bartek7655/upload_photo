import io
import os

from celery import shared_task
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image as ImagePIL

from .models import BinaryImage, SizeImageUpload, Image


@shared_task
def resize_image_async(image_id, sizes):
    instance_image = Image.objects.get(id=image_id)
    photo = instance_image.photo
    image = ImagePIL.open(photo)

    for size in sizes:
        name, extension = photo.name.split('.')[0].split('_')[0], photo.name.split('.')[-1]
        ready_name = name + '_' + str(size) + '.' + extension
        if extension == 'jpg':
            extension = 'jpeg'

        width, height = image.size
        new_width, new_height = width / (height / size), size

        resized_image = image.resize((int(new_width), new_height))
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
        print(ready_image)
        SizeImageUpload.objects.create(
            photo=ready_image,
            image_id=image_id
        )

    if not instance_image.user.type_account.originally:
        os.remove(instance_image.photo.path)
        instance_image.photo = None
        instance_image.save()



@shared_task
def delete_expired_binary_links():
    BinaryImage.objects.filter(expired__lte=timezone.now()).delete()
