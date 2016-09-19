from core import Lang, Interpreter

class DungeonTalk(Lang):
	pass


class DoubleTalk(Lang):
	"""
		Define game specific language constructs
	"""

	# extending symbols
	r_atsign		= r'[@]'

	def __init__(self, *args, **kwargs):
		super(DoubleTalk, self).__init__(*args, **kwargs)

		DoubleTalk.bind_keyword('WAIT', DoubleTalk.Wait)
		DoubleTalk.bind_keyword('GO', DoubleTalk.Go)

		DoubleTalk.bind_symbol(DoubleTalk.r_atsign, {
			Lang.r_identifier:	Lang.handler(DoubleTalk.Character),
			None: 				Lang.handler(DoubleTalk.Ego)
		})

		DoubleTalk.bind_keyword('EYES_ONLY', DoubleTalk.EyesOnly)
		DoubleTalk.bind_keyword('UNTIL', DoubleTalk.Until)
		
		#DoubleTalk.bind_keyword('BY', DoubleTalk.By)
		#DoubleTalk.bind_keyword('TUNE', DoubleTalk.Tune)


	# entity

	class Character(Lang.Identifier):
			
		def __repr__(self):
			return '<character>'

	class Ego(Character):
		pass
		
	"""	
	class By(Lang.Parameter):
		
		def __init__(self, *args, **kwargs):
			super(DoubleTalk.By, self).__init__(*args, **kwargs)
		
	
	class Tune(Lang.Parameter):
		
		def __init__(self, *args, **kwargs):
			super(DoubleTalk.Tune, self).__init__(*args, **kwargs)
	"""

	class EyesOnly(Lang.Keyword):

		def type(self):
			return '<eyes-only>'
		
		def parse(self, parser, **kwargs):
			
			self.readers = parser.build(parser.expression())

			return [self, self.readers]

			#self.condition	= parser.build(parser.expression())
			#self.until		= parser.build(parser.clause(DoubleTalk.Until))
			#return [self, self.condition, self.until]
		
		def eval(self, interp, expression):
			print 'EYES ONLY %s' % (self.readers)
		
	class Wait(Lang.Keyword):
		
		def type(self):
			return '<wait>'
		
		def parse(self, parser, **kwargs):
			self.condition	= parser.build(parser.expression())
			self.until		= parser.build(parser.clause(DoubleTalk.Until))
			return [self, self.condition, self.until]
		
		def eval(self, interp, expression):
			c = interp.eval(self.condition)
			u = interp.eval(self.until)
			print "WAITING %s UNTIL %s" % (c, u)


	class Until(Lang.Parameter):
				
		def __init__(self, *args, **kwargs):
			super(DoubleTalk.Until, self).__init__(*args, **kwargs)

	class Go(Lang.Keyword):
		
		def type(self):
			return '<go>'
		
		def parse(self, parser, **kwargs):
			self.destination	= parser.build(parser.expression())
			return [self, self.destination]
		
		def eval(self, interp, expression):
			d = interp.eval(self.destination)
			print "GO %s" % (d)


	"""
	class BuiltIn(Lang.Def):
		def type(self):
			return '<built-in>'
		
		def eval(self, interp, signature):
			return self.bind(signature)

	class Tailed(BuiltIn):
		
		def __init__(self, token, pos=(None,None), binding=None, **kwargs):
			# function binding
			self.bind = binding
			super(DoubleTalk.Tailed, self).__init__(token,pos, **kwargs)	
	"""