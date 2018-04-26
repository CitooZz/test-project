from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    WRITER = 0
    EDITOR = 1

    ROLE_CHOICES = (
        (WRITER, "Writer"),
        (EDITOR, "Editor")
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=EDITOR)

    REQUIRED_FIELD = []

    @property
    def is_writer(self):
        return self.role == User.WRITER

    @property
    def is_editor(self):
        return self.role == User.EDITOR
