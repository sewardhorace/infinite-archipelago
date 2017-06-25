import os
import random
from string import Formatter
from .helpers import Mapper

class Scrambler:

	def __init__(self, data):
		self.data = Mapper(data)
		self.pronouns_map = {
			'n': Mapper({
				'subject':'it',
				'object':'it',
				'determiner':'its',
				'possessive':'its',
				'reflexive':'itself'
			}),
			'm': Mapper({
				'subject':'he',
				'object':'him',
				'determiner':'his',
				'possessive':'his',
				'reflexive':'himself'
			}),
			'f': Mapper({
				'subject':'she',
				'object':'her',
				'determiner':'her',
				'possessive':'hers',
				'reflexive':'herself'
			})
		}

	def __get_field_list(self, text):
		formatter = Formatter()
		fields = []
		for literal_text, field_name, format_spec, conversion in formatter.parse(text):
			if field_name is not None:
				fields.append(field_name)
		return fields

	def __get_field_map(self, field_list):
		field_map = {}
		for field in field_list:
			field_map[field] = self.__random_value(field)
		return field_map

	def __random_value(self, key):
		if key[0].isupper():
			return random.choice(self.data[key.lower()]).capitalize()
		else:
			return random.choice(self.data[key])

	def __format_pronouns(self, text, sex):
		return text.format_map(self.pronouns_map[sex])

	def scramble(self, text, sex='n'):
		field_list_previous = None
		while True:
			field_list_current = self.__get_field_list(text)
			if field_list_current == field_list_previous:
				text = self.__format_pronouns(text, sex)
				return text
			text = text.format_map(self.__get_field_map(field_list_current))
			field_list_previous = field_list_current