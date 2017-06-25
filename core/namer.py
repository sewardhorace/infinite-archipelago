import random
from .chain import Chain
from .helpers import Mapper, random_from_curve

MEAN_NAMES = 2
MIN_NAMES = 1
MAX_NAMES = 4

MEAN_TITLES = -1
MIN_TITLES = 0
MAX_TITLES = 4 #adj honorific *name* the adj nickname

class CharacterNamer:

    def __init__(self, corpus):
        self.generator = Chain(2)
        self.generator.train(corpus)

    def full_name_string(self):
        name = self.__get_names()
        titles_amt = self.__random_amt_titles()
        format_string = self.__title_format_string(name, titles_amt)
        return format_string

    def __get_names(self):
        name = ''
        names_amt = self.__random_amt_of_names()
        for i in range(names_amt):
            name += self.generator.generate(maximum=10) + ' '
        name = name[:-1]
        return name

    def __random_amt_of_names(self):
        return round(random_from_curve(MEAN_NAMES, MIN_NAMES, MAX_NAMES))

    def __random_amt_titles(self):
        return round(random_from_curve(MEAN_TITLES, MIN_TITLES, MAX_TITLES))

    def __title_format_string(self, name, titles_amt):
        titles_all = ['adj1','honorific','adj2','nickname']
        titles_map = {'name':name}
        for t in titles_all:
            titles_map[t] = ''

        random.shuffle(titles_all)
        titles = titles_all[:titles_amt]
        
        suffix = False
        if 'ajd1' in titles:
            titles_map['adj1'] = '{Char_name_adj} '
        if 'honorific' in titles:
            titles_map['honorific'] = '{Char_name_honorific} '
        if 'adj2' in titles:
            titles_map['adj2'] = ' {Char_name_adj}'
            suffix = True
        if 'nickname' in titles:
            titles_map['nickname'] = ' {Char_name_nickname}'
            suffix = True
        if suffix:
            titles_map['the'] = ' the'
        else:
            titles_map['the'] = ''

        pre_formatter = "{adj1}{honorific}{name}{the}{adj2}{nickname}"
        title_formatter = pre_formatter.format_map(titles_map)
        return title_formatter

# with open("corpora/char_names_3.txt") as f:
#     corpus = f.read().lower().split()

# print(test.full_name_string())


