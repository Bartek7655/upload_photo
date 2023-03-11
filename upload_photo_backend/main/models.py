from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import uniq_path_original_image, uniq_path_new_size_image


class User(AbstractUser):
    type_account = models.ForeignKey(
        "TypeAccount",
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_groups"
    )


class TypeAccount(models.Model):
    name = models.CharField(max_length=100)
    originally = models.BooleanField(default=False)
    binary = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SizeImage(models.Model):
    height = models.IntegerField()
    width = models.IntegerField()
    type_account = models.ManyToManyField(TypeAccount, related_name='sizes')

    def __str__(self):
        return str(self.height)


class BinaryImage(models.Model):
    expired = models.DateTimeField()
    image_binary = models.BinaryField()
    image = models.ForeignKey("Image", on_delete=models.CASCADE, related_name='binary_link')


class Image(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="images"
    )
    created = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(
        null=True,
        upload_to=uniq_path_original_image
    )

    def save(self, *args, **kwargs):
        photo_bytes = self.photo.read()
        type_account = self.user.type_account

        if not type_account.originally:
            self.photo = None
        super().save(*args, **kwargs)

        from .tasks import resize_image_async
        resize_image_async.delay(self.id, photo_bytes, type_account.sizes.all())


class SizeImageUpload(models.Model):
    photo = models.ImageField(
        upload_to=uniq_path_new_size_image
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='different_picture_sizes'
    )
