from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Tasks(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='tasks',
        blank=True, null=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.PositiveSmallIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()


class Tags(models.Model):
    title = models.CharField(max_length=255)
    tasks = models.ManyToManyField(Tasks)


class Category(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='categories')
