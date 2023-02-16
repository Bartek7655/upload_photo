import io

from django.db import models
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from PIL import Image as ImagePIL


class TypeAccount(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='user')


class SizeImage(models.Model):
    binary_link = models.BooleanField(default=False)
    length = models.IntegerField()
    width = models.IntegerField()
    type_account = models.ManyToManyField(TypeAccount, related_name='sizes')


class Image(models.Model):
    image = models.ImageField(upload_to='images')

    def save(self, *args, **kwargs):
        original_image = ImagePIL.open(self.image)

        resized_image = original_image.resize((100, 100))
        buffer_one = io.BytesIO()
        resized_image.save(buffer_one, format="JPEG")
        buffer_one.seek(0)
        content_one = ContentFile(buffer_one.read())

        resized_image_200 = original_image.resize((200, 200))
        two = io.BytesIO()
        resized_image_200.save(two, format="JPEG")
        two.seek(0)
        content_two = ContentFile(two.read())

        self.image.save(f"{self.image.name}.jpg", content_one, save=False)
        self.image.save(f"{self.image.name}200.jpg", content_two, save=False)

        super().save(*args, **kwargs)

