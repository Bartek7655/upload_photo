from django.apps import apps
from django.core.management import call_command
from django.db.models.signals import post_save, post_migrate, pre_save
from django.dispatch import receiver
from PIL import Image as ImagePIL

from .models import Image
from .tasks import resize_image_async


# @receiver(post_save, sender=Image)
# def save_image(sender, instance, **kwargs):
#     resize_image_async(instance)
#     print('tu')
#     if instance.user.type_account.originally:
#         instance.photo = None


# @receiver(post_save, sender=Image)
# def resize_image(sender, instance, **kwargs):
#     resize_image_async.delay(instance.id)


@receiver(post_migrate)
def add_initial_tiers(sender, **kwargs):
    type_account = apps.get_model('main', 'TypeAccount')
    size_image = apps.get_model('main', 'SizeImage')
    if type_account.objects.count() == 0 and size_image.objects.count() == 0:
        call_command('loaddata', 'initial_data.json')
