from django.apps import apps
from django.core.files.base import ContentFile
from django.core.management import call_command
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from PIL import Image as ImagePIL
import io

from .models import Image, BinaryImage


@receiver(post_save, sender=Image)
def resize_image(sender, instance, **kwargs):
    type_account = instance.user.type_account

    for size in type_account.sizes.all():
        img = io.BytesIO(instance.photo.read())
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


@receiver(post_migrate)
def add_initial_tiers(sender, **kwargs):
    TypeAccount = apps.get_model('main', 'TypeAccount')
    SizeImage = apps.get_model('main', 'SizeImage')
    if TypeAccount.objects.count() == 0 and SizeImage.objects.count() == 0:
        call_command('loaddata', 'initial_data.json')

