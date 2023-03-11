from django.contrib import admin

from .models import Image, TypeAccount, SizeImage, User

admin.site.register(Image)
admin.site.register(TypeAccount)
admin.site.register(SizeImage)
admin.site.register(User)
