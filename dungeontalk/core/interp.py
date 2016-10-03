from parser import Parser

OPERAND_L	= 0
OPERATOR 	= 1
OPERAND_R	= 2

class Interpreter(object):
	"""
	Reads language and executes it, handling values stored in memory, etc
	"""

	# default generic language definition
	#lang = Lang()

	@staticmethod
	class EOF:
		pass
		
	class Memory(object):

		def __init__(self):
			self.instr 	= []
			self.stack	= []
			self.scope 	= [{}]

		def get_current_scope(self):
			return self.scope[-1]

		def push_scope(self, namespace={}):
			"""
			Open a scope
			"""
			scp = namespace.copy()
			scp.update(self.get_current_scope())
			self.scope.append(scp)
		
		def pull_scope(self):
			"""
			Remove a scope
			"""
			return self.scope.pop()

		def get_stack(self):
			return self.stack

		def get_stack_top(self):
			return self.stack[-1]
		
		def stack_push(self, v):
			self.stack.append(v)
	
		def stack_pull(self):
			return self.stack.pop()

		def get_instruction(self, address):
			try:	
				return self.instr[address]
			except IndexError as err:
				return False

		def get_all_instructions(self):
			return self.instr
			
		def push_instruction(self, instruction):
			self.instr.append(instruction)
			return self

		def read(self, identifier):
			return self.get_current_scope().get(identifier, None)

		def write(self, identifier, value):
			self.get_current_scope()[identifier] = value
			return self

	def read(self, source, is_file=False):
		"""
		Feeds parser with command
		"""
		self.parser.set_source(source, is_file)
		self.load()
		return self
		
	def load(self):
		"""
		Build grammar tree for all instructions loaded in parser and stores
		it into memory for later execution
		"""
	
		while True:
			instr = self.parser.parse()
			
			if instr is False or instr is None:
				return False

			#build grammar tree
			gtree = self.parser.build(instr)
			
			# append to instruction memory block
			self.memory.push_instruction(gtree)
			#self.memory.instr.append(gtree)

		
	def exec_all(self, source=[], build=True):
		"""
		Execute all lines in source code
		"""
		for i in source:
			r = self.eval(i) if build is None else self.eval(self.parser.build(i))
			self.last = r
			
		return r

	def get_next_instruction(self):
		return self.memory.get_instruction(address=self.pntr)

	def clear(self):
		self.memory			= Interpreter.Memory()
		self.ctrl_stack		= [True]
		self.block_stack	= ['<main>']
		self.pntr 			= 0
		self.last 			= None
	
	def exec_next(self):
		"""
		Executes one line at a time
		"""
		try:
			if self.debug:
				print Interpreter.Snapshot(self)
		except:
			pass
		
		instruction = self.memory.get_instruction(address=self.pntr)

		if instruction is False:
			return self.EOF()

		# eval the instructions	
		r = self.eval(instruction)
		self.last = r
	
		self.pntr += 1
		return r
		
	def bind(self, identifier, value):
		"""
		Bind a variable with a value
		"""

		if isinstance(identifier, self.lang.Identifier):
			
			if identifier.data_type is not None:
				value = identifier.data_type(value, (None, None))

			identifier = identifier.word

		self.memory.write(identifier, value)
	
	def fetch(self, identifier):
		"""
		Get a value from a variable in scope
		"""
		if isinstance(identifier, self.lang.Identifier):
			identifier = identifier.word

		return self.memory.read(identifier)
	
	def call(self, routine, arguments):
		"""
		Handle procedure calls
		"""
		#print 'Calling routine %s' % (routine.get_identifier())

		# push block
		self.push_block(routine)
		
		# address & get signarure
		address = routine.address
		signature = routine.get_signature()
	
		# check signature match with arguments		
		if len(signature) != len(arguments):
			raise Exception('Function expects %s arguments. Given %s' % (len(signature), len(arguments)))
		
		self.memory.push_scope()
		
		if len(signature) > 0:
			# assign calling args to routine signature
			for k,v in enumerate(self.getval(signature)):
				self.bind(self.eval(v), list(arguments)[k])
		
		# is function. Return last statement eval
		if isinstance(routine, self.lang.Def):
			ret = self.exec_all(routine.block)
			#print ret
			self.endcall()
			return ret
		# is procedure. Return nothing. Move instruction pointer
		else:
			# push return address to stack
			self.memory.stack_push({'ret_addr': self.pntr})
			self._goto(address)
		
		
	def endcall(self):
		"""
		Handle procedure call ending
		"""
		ret_addr = None
		
		if len(self.memory.stack) > 0:
			stack = self.memory.stack_pull()
			ret_addr = stack.get('ret_addr', None)
		
		self.endblock()
		self.memory.pull_scope()
				
		if ret_addr is None:
			return
		
		self._goto(ret_addr)	
	
	
	def endblock(self):
		"""
		Close a code of block
		"""
		self.pull_block()
		
	def endif(self):
		"""
		Close an IF statement
		"""
		self.pull_read_enabled()
		self.endblock()
		
	def block(self):
		"""
		Get current block
		"""
		return self.block_stack[-1]
	
	def push_block(self, block):
		"""
		Open a block of code
		"""
		if not isinstance(block, self.lang.Block):
			raise Exception('Tried to push a non-block statement')
		self.block_stack.append(block)
	
	def pull_block(self):
		"""
		Close a block of code
		"""
		return self.block_stack.pop()
	
	def is_read_enabled(self):
		"""
		Returns whether the interpreter is set to execute instructions or to ignore them 
		"""
		return self.ctrl_stack[-1]
	
	def toggle_read_enabled(self):
		"""
		Toggle read enable. Used in IF/ELSE blocks
		"""
		# if parent block isn't executable, child blocks aren't neither
		if not self.ctrl_stack[-2:-1][0]: 
			self.ctrl_stack[-1] = False
		else:
			self.ctrl_stack[-1] = not self.ctrl_stack[-1]
		
	def push_read_enabled(self, boolean):
		"""
		Set a block to be read enabled or not
		"""
		# if parent block isn't executable, child blocks aren't neither
		if not self.is_read_enabled():
			self.ctrl_stack.append(False)
		else:
			self.ctrl_stack.append(boolean)
	
	def pull_read_enabled(self):
		"""
		Remove read enabled property in block
		"""
		return self.ctrl_stack.pop()
	
	# absolute addressing
	def _goto(self, n):
		"""
		Goto absolute address
		"""
		self.pntr = n;
	
	# relative addressing
	def _move(self, i):
		"""
		Move interpreter instruction pointer. Relative address from current pointer position
		"""
		self.pntr += i
	

	"""
	Eval variables, lists. Handle references
	"""
	def getval(self, i, **kwargs):
		
		# it's nested
		if isinstance(i, list) and not isinstance(i, self.lang.List):	
			return self.getval(i.pop(), **kwargs)
		# identifiers
		if isinstance(i, self.lang.Identifier):
			
			# return memory address identifier
			if kwargs.get('ref', None) is not None:
				return i
			# return value in memory
			else:
				return i.eval(self.memory.get_current_scope())
		
		# structs
		elif isinstance(i, self.lang.Vector):
			return i
		
		# constants
		elif isinstance(i, self.lang.Constant):
			return i.eval()
		# a value
		else:
			return i
	
	"""
	Eval sentences
	"""
	def eval(self, i, ref=False):
	
		if isinstance(i, self.lang.List):
			for k,v in enumerate(i):
				i[k] = self.eval(v) if ref is True else self.getval(self.eval(v))
			return i
			
		if isinstance(i, list) and len(i) > 0:
		
			# a control struct
			if isinstance(i[OPERAND_L], self.lang.Control):
				return i[OPERAND_L].eval(self, i[1:])
			
			# ignore is read is not enabled
			if not self.is_read_enabled():
				return None
			
			# a keyword
			if isinstance(i[OPERAND_L], self.lang.Keyword):
				return i[OPERAND_L].eval(self, i[1:])
	
			# expressions
			for k,v in enumerate(i):
				if isinstance(v, list):
					i[k] = self.eval(v)
										
			# a value
			if len(i) < 2:
				return i.pop()
			
			# unary operation
			if len(i) < 3:
				return i.pop(0).eval(self.memory.get_current_scope(), arguments=i.pop(0), interp=self)
			
			# assign operations
			if isinstance(i[OPERATOR], self.lang.Assign):
				return i[OPERATOR].eval(
					left=i[OPERAND_L], 
					right=self.getval(i[OPERAND_R]), 
					heap=self.memory.get_current_scope(),
					interp=self)
			# any other binary operation
			else:
				return i[OPERATOR].eval(
					left=self.getval(i[OPERAND_L]), 
					right=self.getval(i[OPERAND_R]), 
					heap=self.memory.get_current_scope(),
					interp=self)
				
		else:
			return i

	class Snapshot(dict):
		"""
		Takes a snapshot of interpreter state. Print human-readable dump
		"""
		def __init__(self, *args, **kwargs):
			
			interp = args[0]
	
			d = {
				'Pointer': 		interp.pntr,
				'Block stack': 	interp.block_stack,
				'Scope': 		interp.memory.scope,
				'Stack': 		interp.memory.stack,
				'Ctrl stack':	interp.ctrl_stack,
				'Instruction':	interp.memory.instr[interp.pntr],
				'Last result':	interp.last
			}
			
			super(Interpreter.Snapshot, self).__init__(d, **kwargs)
	
		def __str__(self):
			# one-liner aligning with spaces
			return '\n' + '\n'.join(['%s %s %s' % (k, ' ' * (16 - len(k)), v) for k,v in self.iteritems()])


	def __init__(self, lang, debug=False):
		self.lang 	= lang
		self.parser = Parser(self.lang)
		self.debug 	= debug
		self.clear()