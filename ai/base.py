from dungeontalk.core.interp import Interpreter
from dungeontalk import DungeonTalk
from knowledge import Knowledge, FileSystem, Program

class Automaton(object):
	
	def __init__(self, *args, **kwargs):
		self.knowledge 		= Knowledge()
		self.interpreter 	= Interpreter(lang = DungeonTalk())
		self.instructions 	= []

	def add_instruction(self, instruction):
		self.instructions.append(instruction)
		return self

	def set_context(self):
		return self

	def clear_context(self):
		return self

	def get_instructions(self):
		return self.instructions


class AI(object):
	pass