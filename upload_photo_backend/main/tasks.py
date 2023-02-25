import io

from celery import shared_task
from django.core.files.base import ContentFile
from PIL import Image as ImagePIL

from .models import Image

from time import sleep


@shared_task()
def resize_image_async(instance_id):
    instance = Image.objects.get(id=instance_id)
    type_account = instance.user.type_account
    image_binary = instance.photo.read()

    for size in type_account.sizes.all():
        sleep(20)
        img = io.BytesIO(image_binary)
        original_image = ImagePIL.open(img)
        resized_image = original_image.resize((size.width, size.height))
        buffer = io.BytesIO()
        resized_image.save(
            buffer,
            format="jpeg"
        )
        buffer.seek(0)
        ready_image = ContentFile(buffer.getvalue())
        path = f"{instance.photo.url}.{size.height}.jpeg"
        instance.photo.save(path, ready_image, save=False)
