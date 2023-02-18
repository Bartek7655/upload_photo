from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from .utils import uniq_path


class TypeAccount(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='type_account')


class SizeImage(models.Model):
    binary_link = models.BooleanField(default=False)
    expiring_time = models.IntegerField(
        validators=[
            MinValueValidator(300),
            MaxValueValidator(30000)
        ]
    )
    height = models.IntegerField()
    width = models.IntegerField()
    type_account = models.ManyToManyField(TypeAccount, related_name='sizes')


class Image(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="images"
    )
    photo = models.ImageField(upload_to=uniq_path)
