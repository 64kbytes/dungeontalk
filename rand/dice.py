import random

class Dice(object):
	def __init__(self, sides):
		self.sides = sides

	def roll(self):
		return random.choice(range(1,self.sides))

	def __repr__(self):
		return 'd%s' % (self.sides)

class Roll(object):
	def __init__(self, dices):
		self.dices = dices
		self.dices.sort(key=lambda x: x.sides, reverse=True)

	def roll(self):
		return sum([dice.roll() for dice in self.dices])

	def __repr__(self):
		return ' '.join([str(dice) for dice in self.dices])