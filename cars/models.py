
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.CharField(max_length=255)
    images = models.ImageField(upload_to='car_images/', null=True, blank=True)

    def __str__(self):
        return self.title
