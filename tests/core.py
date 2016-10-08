import unittest, os, logging
from dungeontalk import DoubleTalk
from dungeontalk.core import Interpreter

class InterpreterTest(unittest.TestCase):
	
	def setUp(self):
		self.interpreter = Interpreter(lang=DoubleTalk(), debug=True)

	def clear(self):
		self.interpreter.clear()

	def test_value_n_reference(self):

		self.interpreter.read(os.path.dirname(os.path.realpath(__file__)) + '/scripts/functions.dtk', is_file=True)

		#print self.interpreter.memory.get_all_instructions()

		
		while True:
			if isinstance(self.interpreter.exec_next(), Interpreter.EOF):
				break
		
		self.clear()
		print 80*'='

