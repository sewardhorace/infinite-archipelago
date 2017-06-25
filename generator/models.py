from django.db import models


class Character(models.Model):
    char_name = models.CharField(max_length=200)
    char_description = models.TextField()
    char_notes = models.TextField()
