import re

# 	TODO 
#	weird delimiter characters behavior 
#	check for Evaluable & Callable classes

class Lang(object):
	"""
		Generic language definition
	"""

	delimiters = "[\"\':!,;+*^&@#$%&\-\\/\|=$()?<>\s\[\]]"
	
	r_space 		= r'[ ]'
	r_newline		= r'[\n]'
	r_tab 			= r'[\t]'
	r_slash 		= r'[/]'
	r_asterisk 		= r'[*]'
	r_comma 		= r'[,]'
	r_equal 		= r'[=]'
	r_plus 			= r'[+]'
	r_dash 			= r'[-]'
	r_bracket_l 	= r'[\[]'
	r_bracket_r		= r'[\]]'
	r_parentheses_l = r'[(]'
	r_parentheses_r	= r'[)]'
	r_hash 			= r'[#]'
	r_bang 			= r'[!]'
	r_question		= r'[?]'
	r_double_quote 	= r'[\"]'
	r_single_quote 	= r"[\']"
	r_float			= r'^[0-9]*\.[0-9]+$'
	r_int	 		= r'^[0-9]+$'
	r_not 			= r'^NOT$'
	r_identifier 	= r'[_a-zA-Z][_a-zA-Z0-9]*'
	
	symbols = {
		r_space: 			lambda w,t: Lang.Space(w,t),
		r_newline:			lambda w,t: Lang.NewLine(w,t),
		r_tab:				lambda w,t: Lang.Tab(w,t),
		r_bracket_l: 		lambda w,t: Lang.Bracket(w,t, open=True),
		r_bracket_r:		lambda w,t: Lang.Bracket(w,t, open=False),
		r_double_quote: 	lambda w,t: Lang.DoubleQuote(w,t),
		r_single_quote: 	lambda w,t: Lang.SingleQuote(w,t),
		r_parentheses_l: 	lambda w,t: Lang.Parentheses(w,t, open=True),
		r_parentheses_r:	lambda w,t: Lang.Parentheses(w,t, open=False),
		r_slash: {
			r_asterisk:		lambda w,t: Lang.CommentBlock(w,t, open=True),
			r_slash: 		lambda w,t: Lang.CommentLine(w,t),
			None:			lambda w,t: Lang.Divide(w,t)
		},
		r_asterisk: {
			r_slash:		lambda w,t: Lang.CommentBlock(w,t, open=False),
			None:			lambda w,t: Lang.Multiply(w,t)
		},
		r_comma: 			lambda w,t: Lang.Comma(w,t),
		r_bang: {
			r_equal: {
				r_equal:	lambda w,t: Lang.InequalStrict(w,t),
				None:		lambda w,t: Lang.Inequal(w,t)
			},
			None: 			lambda w,t: Lang.Assign(w,t)
		},
		r_equal: {
			r_equal: {
				r_equal:	lambda w,t: Lang.EqualStrict(w,t),
				None:		lambda w,t: Lang.Equal(w,t)
			},
			None: 			lambda w,t: Lang.Assign(w,t)
		},
		r_plus: {
			r_plus:			lambda w,t: Lang.Increment(w,t),
			None:			lambda w,t: Lang.Add(w,t)
		},
		r_float: 			lambda w,t: Lang.Float(w,t),
		r_int: 				lambda w,t: Lang.Integer(w,t),
		r_dash: {
			r_dash:			lambda w,t: Lang.Decrement(w,t),
			r_float: 		lambda w,t: Lang.Float(w,t),
			r_int: 			lambda w,t: Lang.Integer(w,t),
			None:			lambda w,t: Lang.Subtract(w,t)
		},
		r_not:				lambda w,t: Lang.Not(w,t),
		r_identifier:		lambda w,t: Lang.identifier(w,t),
	}

	data_types = {
		'String':	lambda w,t: Lang.DataType(w,t),
		'Integer':	lambda w,t: Lang.DataType(w,t),
		'Float':	lambda w,t: Lang.DataType(w,t),
		'List':		lambda w,t: Lang.DataType(w,t),
	}

	keywords = {
		'prnt':			lambda w,t: Lang.Prnt(w,t),
		'if':			lambda w,t: Lang.If(w,t),
		'else':			lambda w,t: Lang.Else(w,t),
		'end':			lambda w,t: Lang.End(w,t),
		'procedure':	lambda w,t: Lang.Procedure(w,t),
		'def':			lambda w,t: Lang.Def(w,t),
		'ret': 			lambda w,t: Lang.Ret(w,t),
		'exec':			lambda w,t: Lang.Exec(w,t),
		'include':		lambda w,t: Lang.Include(w,t),
	}
	
	parameters = {
		#'UNTIL':		lambda w,t: Lang.Until(w,t),
		#'BY':			lambda w,t: Lang.By(w,t),
		#'TUNE':		lambda w,t: Lang.Tune(w,t),
	}
	
	# A clause is a keyword acting as a parameter for another keyword 
	clause = {
		r'<parameter>':	lambda: Lang.expression
	}

	expression = {
		r'<unary-op>': lambda: Lang.expression,
		r'<delim>|<bracket>': lambda: Lang.expression,
		r'<const>|<ident>': {
			r'<bracket>|<const>|<ident>': lambda: Lang.expression[r'<const>|<ident>'],
			'<op>': lambda: Lang.expression,
			'</delim>|</bracket>': lambda: Lang.expression[r'<const>|<ident>'],
			'<comma>': lambda: Lang.expression
		},
		r'<datatype>': lambda: Lang.expression,
	}

	@staticmethod
	def identifier(w,t):
		if w in Lang.keywords:
			return Lang.keywords[w](w,t)
		elif w in Lang.parameters:
			return Lang.parameters[w](w,t)
		elif w in Lang.data_types:
			return Lang.data_types[w](w,t)
		else:
			return Lang.Identifier(w,t)

	@staticmethod
	def bind_keyword(keyword, cls):
		Lang.keywords[keyword] = Lang.handler(cls)

	@staticmethod
	def bind_parameter(parameter, cls):
		Lang.parameters[parameter] = Lang.handler(cls)

	@staticmethod
	def bind_symbol(symbol, sequence):
		Lang.symbols[symbol] = sequence

	@staticmethod
	def handler(cls, **kwargs):
		return lambda w,t: cls(w,t, **kwargs)

	class Evaluable(object):
		pass
	
	class Callable(object):

		def get_signature(self):
			return self.signature
	
	# keywords
	class Block(object):
		def __init__(self, *args, **kwargs):
			self.length = 0
			self.owner = None
	

	class Control(object):
		pass
	
		
	class Lexeme(object):
		"""
		Base class for every language word
		"""
		
		def __init__(self, word=None, pos=(None,None), **kwargs):
			self.word = word
			self.line, self.char = pos
			self.set(kwargs)
			
		def set(self, kwargs):
			"""
			Convenience method for setting properties dinamically
			"""
			for i in kwargs:
				setattr(self, i, kwargs[i])
		
		def type(self):
			raise NotImplementedError

		def parse(self, parser, **kwargs):
			raise NotImplementedError

		def eval(self, scope, arguments=None, interp=None):
			raise NotImplementedError

		def __repr__(self):
			return '<%s><%s>' % (self.__class__.__name__, self.word)

	class WhiteSpace(Lexeme):
		"""
		Spaces and tabs 
		"""
		pass

	class Space(WhiteSpace):
		pass

	class NewLine(WhiteSpace):
		def type(self):
			return '<newline>'

	class Tab(WhiteSpace):
		pass


	# base types

	class Vector(Lexeme):
		def type(self):
			return '<struct>'
			
	class Constant(Lexeme):
		def type(self):
			return '<const>'
			
		def __repr__(self):
			return '<const %s>' % (self.word)

	class String(str, Constant):
		def __init__(self, string, pos=(None,None)):
			super(Lang.String, self).__init__(string, pos)
		
		def __new__(cls, *args, **kw):
			string,pos = args
			return  super(Lang.String, cls).__new__(cls, string)
			
		def eval(self):
			return str(self)

		def __repr__(self):
			return '<string %s>' % (self.word)
	

	class Float(float, Constant):
		
		def __init__(self, number, pos=(None,None)):
			super(Lang.Float, self).__init__(number, pos)
		
		def __new__(cls, *args, **kw):
			number,pos = args
			return  super(Lang.Float, cls).__new__(cls, number)

		def eval(self):
			return self
	
	class Integer(int, Constant):
		
		def __init__(self, number, pos=(None,None)):
			super(Lang.Integer, self).__init__(number, pos)
		
		def __new__(cls, *args, **kw):
			number,pos = args
			return  super(Lang.Integer, cls).__new__(cls, number)

		def eval(self):
			return self
	
	class List(list, Vector):
	
		def __init__(self, l=[]):
			list.__init__(self, l)
			
		def type(self):
			return '<list>'
			
		def __add__(self, other):
			return Lang.List(list.__add__(self, other))
		
		def __getitem__(self, item):
			result = list.__getitem__(self, item)
			try:
				return Lang.List(result)
			except TypeError:
				return result
        	
		def eval(self):
			return self
		
	# operators
	class Operator(Lexeme):
		def type(self):
			return '<op>'

		def __repr__(self):
			return '<op %s>' % (self.word)
		
		def eval(self, left, right, interp):
			raise NotImplementedError
	
	class UnaryOperator(Operator):
		def type(self):
			return '<unary-op>'

		def __repr__(self):
			return '<unary-op %s>' % (self.word)
		
		def eval(self, operand):
			raise NotImplementedError
	
	class Not(UnaryOperator):
		def eval(self, scope, arguments=None, interp=None):
			return not interp.getval(interp.eval(arguments))

	class Assign(Operator):

		def eval(self, left, right, heap, interp):
			
			interp.bind(identifier=left, value=right)
			#heap[left.word] = right
			return left

	class Equal(Operator):
		def eval(self, left, right, heap, interp):
			return left == right

	class Inequal(Operator):
		def eval(self, left, right, heap, interp):
			return left != right

	class EqualStrict(Operator):
		pass
	
	class InequalStrict(Operator):
		pass

	class Subtract(Operator):
		def eval(self, left, right, heap, interp):
			return left - right

	class Add(Operator):
		def eval(self, left, right, heap, interp):
			try:
				return left + right
			except TypeError:
				raise

	class Increment(Operator):
		def eval(self, left):
			pass

	class Decrement(Operator):
		def eval(self, left):
			pass

	class Divide(Operator):
		def eval(self, left, right, heap, interp):
			return left / right

	class Multiply(Operator):
		def eval(self, left, right, heap, interp):
			return left * right

	# delimiters
	class Delimiter(Lexeme):
		pass
	
	# expression delimiters	
	class Parentheses(Delimiter):
		
		def type(self):
			return '<delim>' if self.open else '</delim>'

		def __repr__(self):
			return '<delim>' if self.open else '</delim>'
			
	class Bracket(Delimiter):
		
		def type(self):
			return '<bracket>' if self.open else '</bracket>'

		def __repr__(self):
			return '<bracket>' if self.open else '</bracket>'
	
	# list delimiter
	class Comma(Delimiter):
		
		def type(self):
			return '<comma>'

		def __repr__(self):
			return '<comma>'
	
	# string delimiters
	class DoubleQuote(Delimiter):
		
		def type(self):
			return '<d-quote>'

		def __repr__(self):
			return '<d-quote>'
	
	class SingleQuote(Delimiter):
		
		def type(self):
			return '<s-quote>'

		def __repr__(self):
			return '<s-quote>'
	

	class DataType(Lexeme):

		def type(self):
			return '<datatype>'

		def eval(self, scope, arguments=None, interp=None):

			if hasattr(Lang, self.word):
				the_type = getattr(Lang, self.word)

			arguments.set_data_type(the_type)

			return arguments

		def __init__(self, word, pos=(None,None), **kwargs):
			self.word = word
			self.line, self.char = pos
			self.set(kwargs)
			
		def __repr__(self):
			return '<datatype %s>' % (self.word)

	# identifiers
	class Identifier(Lexeme):

		def __init__(self, *args, **kwargs):
		
			self.data_type = None
			super(Lang.Identifier, self).__init__(*args, **kwargs)
		
		def type(self):
			return '<ident>'

		def set_data_type(self, data_type):
			self.data_type = data_type
		
		def eval(self, scope, arguments=None, interp=None):
			
			v = scope.get(self.word, None)
			if arguments is not None and v is not None:
				return v.call(arguments, interp)
			else:
				return v

		def __repr__(self):
			return "<Identifier(%s)>%s" % (self.data_type, self.word)	
	
	class Keyword(Lexeme):

		def get_identifier(self):
			return self.identifier
		
		def type(self):
			return '<keyword>'
			
		def __repr__(self):
			return '<%s>' % (self.word)
			
	
	class Procedure(Keyword, Callable, Block,Control):

		def __init__(self, word, pos=(None,None), **kwargs):
			self.address	= None
			self.identifier = None
			self.signature 	= Lang.List()
			super(Lang.Procedure, self).__init__(word, pos=(None,None), **kwargs)
			
		def type(self):
			return '<procedure>'
		
		def parse(self, parser, **kwargs):	
			#print 'Procedure is being parsed'

			# parse identifier
			i = parser.next()
			if not isinstance(i, Lang.Identifier):
				raise Exception('Procedure must have an identifier')
			else:
				self.identifier = [i]
			
			try:
				# get arguments
				self.signature = parser.build(parser.expression())

			except Exception as e:
				self.signature = Lang.List()
							
			return [self, self.identifier, self.signature]
		
		def eval(self, interp, signature):
			#print "Procedure is being eval'd"

			# store procedure address
			self.address = interp.pntr

			# eval procedure identifier, leaving room for dynamic procedures
			self.identifier = interp.getval(self.identifier, ref=False)
				
			# store identifier & memory address
			interp.bind(self.identifier.word, self)
			
			# skip function block. We are just declaring the function		
			interp._move(self.length+1)
		
		def call(self, arguments, interp):
			return interp.call(self, arguments)
			

	class Def(Procedure):
		"""
		Unlike procedures, functions stores its code block
		"""
		def __init__(self, word, pos=(None,None), **kwargs):
			self.block = []
			super(Lang.Procedure, self).__init__(word, pos=(None,None), **kwargs)

		def parse(self, parser, **kwargs):	
			# parse identifier
			self.identifier = [parser.next()]			
			
			try:
				# get arguments
				self.signature = parser.build(parser.expression())

			except Exception as e:
				self.signature = Lang.List()

			nesting = parser.get_nesting_level()
				
			# get function block
			self.block = parser.block(until=Lang.End(nesting=nesting))

			return [self, self.identifier, self.signature]

		def eval(self, interp, signature):
	
			# store procedure address
			self.address = interp.pntr

			# eval procedure identifier, leaving room for dynamic procedures
			self.identifier = interp.getval(self.identifier, ref=False)
					
			# store identifier & memory address
			interp.bind(self.identifier.word, self)
		
		def call(self, arguments, interp):			
			return interp.call(self, arguments)

	class Ret(Keyword):
		
		def type(self):
			return '<ret>'

		def parse(self, parser, **kwargs):
			self.expression = parser.build(parser.expression())
			return [self, self.expression]
		
		def eval(self, interp, expression):	
			self.value = interp.getval(interp.eval(self.expression))
			return self

	class Exec(Keyword):
		
		def type(self):
			return '<exec>'
		
		def parse(self, parser, **kwargs):
			
			identifier = [parser.next()]			
			
			try:
				arguments = parser.build(parser.expression())
			except Exception as e:
				arguments = Lang.List()
				
			return [self, identifier, arguments]
		
		def eval(self, interp, signature):
		
			# get arguments if any
			arguments = interp.eval(signature.pop()) if len(signature) > 1 else []
		
			# get identifier from instruction line
			identifier = interp.getval(signature.pop(), ref=True)
			
			# get procedure from scope
			routine = interp.fetch(identifier)
			
			if not isinstance(routine, Lang.Callable):
				raise Exception('Not a callable object')
		
			return interp.call(routine, arguments)
			
	
	class If(Keyword,Block,Control):
	
		def type(self):
			return '<if>'

		def parse(self, parser, **kwargs):
			# store condition pre-built
			condition = parser.build(parser.expression(until=Lang.NewLine))
			return [self, condition]
		

		def eval(self, interp, expr):
			# if condition is truthly, interpreter executes the following block
			interp.push_read_enabled(bool(interp.eval(expr)))
			interp.push_block(self)
	
	
	class Else(Keyword,Control):
		
		def type(self):
			return '<else>'
		
		def parse(self, parser, **kwargs):
			return [self]
			
		def eval(self, interp, expr):
			# if last block was executed following will not, and viceversa
			interp.toggle_read_enabled()

	
	class End(Keyword,Control,Delimiter):

		def __init__(self, *args, **kwargs):
			self.nesting = kwargs.get('nesting', None)
			super(Lang.End, self).__init__(*args, **kwargs)
		
		def type(self):
			return '<end>'
			
		def parse(self, parser, **kwargs):
			return [self]
		
		def eval(self, interp, expr):
		
			block = interp.block()
			
			if isinstance(block, Lang.If):
				interp.endif()
			elif isinstance(block, Lang.Procedure):
				#print 'Ending procedure block'
				interp.endcall()
			elif isinstance(block, Lang.Def):
				#print 'Ending def block'
				interp.endcall()
			else:
				print interp.block_stack
				raise Exception('Unknown block type')
	
	class Parameter(Lexeme):
	
		def __init__(self, *args, **kwargs):
			super(Lang.Parameter, self).__init__(*args, **kwargs)
			
		def eval(self, scope, arguments=None, interp=None):
			return interp.eval(arguments)
			
		def type(self):
			return '<parameter>'
		
		def __repr__(self):
			return '<parameter>'


	class Prnt(Keyword):
		
		def type(self):
			return '<prnt>'

		def parse(self, parser, **kwargs):
			self.text = parser.build(parser.expression())
			return [self, self.text]
		
		def eval(self, interp, expression):
			print interp.getval(interp.eval(self.text))

		def __repr__(self):
			return '<prnt>'
	
	
	"""
	PREPROCESSOR
	
	"""
	class Preprocessor(Lexeme):
		pass
		
	class CommentBlock(Preprocessor, Delimiter):
		pass
	
	class CommentLine(Preprocessor, Delimiter):
		pass

	class Include(Preprocessor, Keyword):
		
		def type(self):
			return '<include>'
			
		def parse(self, parser):
			src = parser.expression()
			return [self, src]

		def eval(self, interp, source):
			print source
			exit(1)
		

	class Grammar(list):
		def __init__(self, rules):
			self.grammar	= rules
			self.legal 		= rules
			super(Lang.Grammar, self).__init__()
		
		# does lexeme belong to this grammar
		@staticmethod
		def belongs(i, grammar):
			branch = grammar
			# iterate through currently legal words	
			for r in branch:	
				if re.match(r, i.type()):
					return True
				elif branch.get(r, None) is not None:
					branch = branch[r] if not callable(branch[r]) else branch[r]()
					
			return False
		
		@staticmethod
		def is_legal(s, grammar):
			rules = grammar
			# iterate through words in sentence
			for i in s:
				# iterate through currently legal words	
				found = False
				for r in rules:
					if re.match(r, i.type()):
						rules = rules[r] if not callable(rules[r]) else rules[r]()
						found = True
						break
					
						
				if not found:
					return False
			return True
		
		def hint(self):
			if self.legal is None:
				return None
			else:
				return self.legal.keys()
		
		def can_push(self, i):
			# iterate through currently legal words	
			for r in self.legal:	
				if re.match(r, i.type()):
					return r
			return False

		def push(self, i):
			# if instruction begins, legal should point to all instruction set
			if len(self) == 0:
				self.legal = self.grammar
				
			l = self.can_push(i)
			#print 'Is legal %s? %s %s %s' % (self.__class__.__name__, i.type(), self.hint(), l)
			# push term
			if l:
				# climb up in grammar tree
				self.legal = self.legal[l] if not callable(self.legal[l]) else self.legal[l]()
				super(Lang.Grammar, self).append(i)	
				return self
				
			# close
			return False
		
	class Clause(Grammar):
		def __init__(self):
			super(Lang.Clause, self).__init__(Lang.clause)
		
		def type(self):
			return '<clause>'
		
	class Expression(Grammar):
		def __init__(self):
			super(Lang.Expression, self).__init__(Lang.expression)
		
		def type(self):
			return '<expression>'

