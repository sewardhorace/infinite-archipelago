import random
from django.db import models


class Character(models.Model):
    char_name = models.CharField(max_length=200)
    char_description = models.TextField()
    char_notes = models.TextField()

    @classmethod
    def generate(cls, scrambler, namer):
      char_format_string = ('- {race} {char_detail_physical}.\n'
        '- {subject} {char_trait_attitude}.\n'
        '- {subject} {char_trait_manner}.\n'
        '- {subject} {char_ability_competency}.\n'
        '- {subject} {char_ability_move}.\n'
        '- {subject} is {char_inventory}.')

      char_name = scrambler.scramble(namer.full_name_string())
      char_description = scrambler.scramble(char_format_string, random.choice(['m', 'f']))
      character = Character(char_name=char_name, char_description=char_description)
      return character

class Room(models.Model):
  height = models.PositiveSmallIntegerField() 
  width = models.PositiveSmallIntegerField()
  x_origin = models.IntegerField()
  y_origin = models.IntegerField()
  room_description = models.TextField()
  room_notes = models.TextField()

  @classmethod
  def generate(cls, scrambler):
    room_format_string = ('- the room is 25ft x 25ft.\n'
        '- {construction}.\n'
        '- {atmosphere}.\n'
        '- {feature}.')

    room_description = scrambler.scramble(room_format_string)
    room = Room(room_description=room_description)
    return room

class Door(models.Model):
  x_origin = models.IntegerField()
  y_origin = models.IntegerField()

class Corridor(models.Model):
  pass