from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .utils import uniq_path


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
    binary_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SizeImage(models.Model):
    height = models.IntegerField()
    width = models.IntegerField()
    type_account = models.ManyToManyField(TypeAccount, related_name='sizes')


class BinaryImage(models.Model):
    expiring_time = models.IntegerField(
        validators=[
            MinValueValidator(300),
            MaxValueValidator(30000)
        ]
    )
    image_binary = models.BinaryField()
    image = models.ForeignKey("Image", on_delete=models.CASCADE, related_name='binary')


class Image(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="images"
    )
    photo = models.ImageField(upload_to=uniq_path)
