import random

class Chain:
	def __init__(self, order):
		self.order = order
		self.group_size = self.order + 1
		self.graph = {}
		self.beginnings = []
		return

	def train(self, corpus):
		for item in corpus:
			self.beginnings.append(item[0:2])
			item += " "

			for i in range(len(item) - self.order):
				key = tuple(item[i:i + self.order])
				value = item[i+self.order]

				if key in self.graph:
					self.graph[key].append(value)
				else:
					self.graph[key] = [value]

	def generate(self, maximum=100):
		start = random.choice(self.beginnings)
		result = start

		while True:
			state = tuple(result[len(result) - self.order:])
			default = random.choice(list(self.graph.keys()))
			next_character = random.choice(self.graph.get(state, default)) #need a fallback for key errors
			if next_character == " ":
				if self.__is_valid__(result):
					return result.title()
				else:
					result = start
				
			else:
				result += next_character
				if len(result) >= maximum and " " in self.graph.get(state, default):
					return result.title()


	def __is_valid__(self, word):
		vowels = {"a", "e", "i", "o", "u"}
		if any(char in vowels for char in word):
			return True
		else:
			return False