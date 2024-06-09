from django.contrib.auth.models import AbstractUser
from django.db import models


def upload_thumbnails(instance, filename):
    path = f'thumbnails/{instance.username}'
    extension = filename.split('.')[-1]
    if extension:
        path = path + '.' + extension
        return path



class User(AbstractUser):
    thumbnails = models.ImageField(
        upload_to=upload_thumbnails,
        null=True,
        blank=True
    )


