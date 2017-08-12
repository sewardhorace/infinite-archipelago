from django.db import models
from django.contrib.postgres.fields import JSONField

class Game(models.Model):
  placeholder = models.TextField()
  # data = JSONField()

  def __str__(self):
    return 'Game ID %s' % (self.pk)

class Component(models.Model):
  game = models.ForeignKey(Game, on_delete=models.CASCADE)
  x = models.IntegerField()
  y = models.IntegerField()
  width = models.PositiveSmallIntegerField()
  height = models.PositiveSmallIntegerField() 
  isActive = models.BooleanField()
  CATEGORY_CHOICES = (
    ('L', 'Location'),
    ('T', 'Transport'),
    ('C', 'Creature'),
    ('P', 'Party'),
  )
  category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)

  def __str__(self):
    return 'ID %s, %s' % (self.pk, self.get_category_display())

class Detail(models.Model):
  component = models.ForeignKey(Component, on_delete=models.CASCADE)
  content = models.TextField()

  def __str__(self):
    return '%s' % (self.content[:50] + "...")
  