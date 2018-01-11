from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from oauth2client.contrib.django_util.models import CredentialsField

from core.helpers import parse_sheet_url

class CredentialsModel(models.Model):
  id = models.OneToOneField(User, primary_key=True)
  credential = CredentialsField()

class Game(models.Model):
  name = models.CharField(max_length=50, default='', blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  scrambler_data = JSONField()
  scrambler_endpoints = JSONField()
  sheet_url = models.URLField(null=True)
  # map_pan
  # map_zoom

  def __str__(self):
    if len(self.name) > 0:
      return '%s' % (self.name)
    else:
      return 'Game ID %s' % (self.pk)

  def sheet_id(self):
    if self.sheet_url:
      return parse_sheet_url(self.sheet_url)
    else:
      return None

class Component(models.Model):
  name = models.CharField(max_length=50, default='', blank=True)
  game = models.ForeignKey(Game, on_delete=models.CASCADE)
  x = models.DecimalField(max_digits=19, decimal_places=15)
  y = models.DecimalField(max_digits=19, decimal_places=15)
  width = models.PositiveSmallIntegerField(default=1, blank=True)
  height = models.PositiveSmallIntegerField(default=1, blank=True)
  isActive = models.BooleanField(default=False)
  LOCATION = 'L'
  PARTY = 'P'
  CREATURE = 'C'
  TRANSPORT = 'T'
  OTHER = 'O'
  CATEGORY_CHOICES = (
    (LOCATION, 'Location'),
    (PARTY, 'Party'),
    (CREATURE, 'Creature'),
    (TRANSPORT, 'Transport'),
    (OTHER, 'Other'),
  )
  category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default=OTHER, blank=True)

  def __str__(self):
    if len(self.name) > 0:
      return '%s (%s)' % (self.name, self.get_category_display())
    else:
      return 'ID# %s (%s)' % (self.pk, self.get_category_display())

class Detail(models.Model):
  component = models.ForeignKey(Component, on_delete=models.CASCADE)
  content = models.TextField(blank=True)

  def __str__(self):
    if len(self.content) > 50:
      return '%s' % (self.content[:50] + "...")
    else:
      return '%s' % (self.content)
  