import random

class Mapper(dict):
	def __missing__(self, key):
		return ['{' + key + '}']

def random_from_curve(mean:int, minimum:int, maximum:int):
    std_deviation = (maximum - mean) / 3
    num = random.gauss(mean, std_deviation)
    if num < minimum:
        num = minimum
    if num > maximum:
        num = maximum
    return num