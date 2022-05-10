from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from phone_field import PhoneField
from django.db.models.signals import post_save
from django.dispatch import receiver


def image_upload(instance, filename):
    ext = filename.split(".")[-1]
    return 'profile/{}.{}'.format(instance.user, ext)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload, default='profile/default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        rgb_img = img.convert('RGB')
        if rgb_img.height > 300 or rgb_img.width > 300:
            output_size = (300, 300)
            rgb_img.thumbnail(output_size)
            rgb_img.save(self.image.path)

