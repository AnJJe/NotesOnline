# notes/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from board.models import Board


class ListNote(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    finished = models.BooleanField(default=False)  # По умолчанию не завершено
    deleted = models.BooleanField(default=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk and not kwargs.get('update_fields') == ['deleted']:
            self.updated_at = timezone.now()  # Manually update `updated_at` only when needed
        super().save(*args, **kwargs)
