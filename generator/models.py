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
  x = models.IntegerField()
  y = models.IntegerField()
  width = models.PositiveSmallIntegerField()
  height = models.PositiveSmallIntegerField() 
  isActive = models.BooleanField()
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

class Corridor(models.Model):
  '''
  path (list of x,y coordinates as tuples?)
  isActive = models.BooleanField()
  corridor_description = models.TextField()
  corridor_notes = models.TextField()
  '''
  pass

class Door(models.Model):
  x = models.IntegerField()
  y = models.IntegerField()
  direction = models.CharField(max_length=5)
  isOpen = models.BooleanField()
  corridor = models.ForeignKey(Corridor, on_delete=models.CASCADE)
  room = models.ForeignKey(Room, on_delete=models.CASCADE)

  '''
  must create and save room and corridor before creating new door for foreign key
  Door(x = x, y = y, direction = 'north', corridor = c, room = r)
  '''

class Sector(models.Model):
  '''
  needs to contain a reference to the corridors that exit its borders, 
  for the purpose of creating the entrance corridors for the neighboring sectors
  '''
  pass