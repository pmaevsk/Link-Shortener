from django.db import models
from django.contrib.auth.models import User


class Link(models.Model):
    original = models.CharField(max_length=100)
    short = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.original