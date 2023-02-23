from django.apps import apps
from django.core.files.base import ContentFile
from django.core.management import call_command
from django.db.models.signals import post_save, post_migrate, pre_delete
from django.dispatch import receiver
from PIL import Image as ImagePIL
import io

from .models import Image, BinaryImage


@receiver(post_save, sender=Image)
def resize_image(sender, instance, **kwargs):
    type_account = instance.user.type_account
    image_binary = instance.photo.read()

    for size in type_account.sizes.all():
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


@receiver(pre_delete, sender=BinaryImage)
def delete_image_file(sender, instance, **kwargs):
    if instance.expiring_time is not None and not instance.is_expired:
        return


@receiver(post_migrate)
def add_initial_tiers(sender, **kwargs):
    type_account = apps.get_model('main', 'TypeAccount')
    size_image = apps.get_model('main', 'SizeImage')
    if type_account.objects.count() == 0 and size_image.objects.count() == 0:
        call_command('loaddata', 'initial_data.json')
