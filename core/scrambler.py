import random
from string import Formatter

#TODO: support for random numbers in the text, i.e., "missing {#1,5} fingers"
#TODO: support for capitalization {Weapon} vs {weapon} (currently does not trickle down if returned string is another {bracketed_word})
class Scrambler:
	def __init__(self, data):
		self.data = data

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
			field_map[field] = self.__get_value(field)
		return field_map

	def __get_value(self, key):
		if key.lower() in self.data:
			if key[0].isupper():
				print(random.choice(self.data[key.lower()]).capitalize())
				return random.choice(self.data[key.lower()]).capitalize()
			else:
				return random.choice(self.data[key])
		else:
			return '{' + key + '}'

	def scramble(self, text):
		field_list_previous = None
		while True:
			field_list_current = self.__get_field_list(text)
			if field_list_current == field_list_previous:
				return text
			text = text.format_map(self.__get_field_map(field_list_current))
			field_list_previous = field_list_current

# input_data = {}
# with open('input_data/data.json') as json_data:
#     input_data = json.load(json_data)

# scrambler = Scrambler(input_data)
# text = scrambler.scramble("Hi, my name is {Item_weapon}")
# print(text)