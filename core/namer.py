import random
from .chain import Chain
from string import Formatter

#TODO: figure out how to do this with inheritance (Scrambler)
class Namer:
    def __init__(self, data):
        #'data' is a dictionary of lists of seed names
        self.generator = Chain(2)
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
        if key in self.data:
            corpus = self.data[key]
            self.generator.train(corpus)
            name = self.generator.generate(maximum=10)
            return name
        else:
            return '{' + key + '}'
        

    def generate(self, text):
        field_list_previous = None
        while True:
            field_list_current = self.__get_field_list(text)
            if field_list_current == field_list_previous:
                return text
            text = text.format_map(self.__get_field_map(field_list_current))
            field_list_previous = field_list_current

        
# input_data = {}
# with open('corpora/data.json') as json_data:
#     input_data = json.load(json_data)

# namer = Namer(input_data)
# text = namer.generate("I cast {name_spell_adj} {name_spell_noun}")
# print(text)