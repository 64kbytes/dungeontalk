from dungeontalk import DoubleTalk, Interpreter
from knowledge import Knowledge, FileSystem, Program

class Automaton(object):
	
	def __init__(self, *args, **kwargs):
		self.knowledge 		= Knowledge()
		self.interpreter 	= Interpreter(lang = DoubleTalk(), debug=True)
		self.instructions 	= []

	def add_instruction(self, instruction):
		self.instructions = instruction
		return self

	def set_context(self):
		return self

	def clear_context(self):
		return self

	def get_instructions(self):
		return self.instructions


class AI(object):
	pass