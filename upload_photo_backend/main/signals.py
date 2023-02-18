from django.core.files.base import ContentFile
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from PIL import Image as ImagePIL
import io

from .models import Image


@receiver(post_save, sender=Image)
def resize_image(sender, instance, **kwargs):
    type_account = instance.user.type_account
    print('instance.user.sizes', type_account.sizes.all())

    for x in range(2):
        img = io.BytesIO(instance.photo.read())
        original_image = ImagePIL.open(img)
        resized_image = original_image.resize((100, 100))
        buffer = io.BytesIO()
        resized_image.save(
            buffer,
            format="jpeg"
        )
        buffer.seek(0)
        ready_image = ContentFile(buffer.getvalue())
        path = f"{instance.photo.url}_{x}.jpeg"
        instance.photo.save(path, ready_image, save=False)
