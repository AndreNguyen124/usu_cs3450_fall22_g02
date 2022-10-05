from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

def get_absolute_url(self):
  return reverse('my_app:my_app', kwargs={'slug': self.slug })
