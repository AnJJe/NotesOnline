from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Board(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, related_name='member_boards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.name

class BoardCode(models.Model):
    board = models.OneToOneField(Board, on_delete=models.CASCADE)
    code = models.CharField(max_length=16)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.board.name}'s code"

