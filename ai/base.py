from knowledge import Knowledge

class Automaton(object):
	
	def __init__(self, *args, **kwargs):
		self.knowledge 		= []
		self.funcitons 		= []
		self.procedures 	= []
		self.instructions 	= ''

	def set_instruction(self, instruction):
		self.instructions = instruction
		return self

	def get_instructions(self):
		return self.instructions

class AI(object):
	pass