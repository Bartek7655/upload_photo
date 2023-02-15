from django.db import models
from django.contrib.auth import get_user_model
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
    image = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = ImagePIL.open(self.image.path)

        img.thumbnail(100, 100)
        img.save(self.image.path.replace(".", "_100x100."), "JPEG")
