from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self) -> str:
        return self.name


class Tasks(models.Model):
    PRIORITY_CHOICES = (
        ('3', '3'),
        ('2', '2'),
        ('1', '1')
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='tasks',
        blank=True, null=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(
        max_length=1, choices=PRIORITY_CHOICES, default='1')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)

    def __str__(self) -> str:
        return self.title
