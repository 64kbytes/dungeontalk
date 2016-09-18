from core.lang import Lang

class DungeonTalk(Lang):
	"""
		Define game specific language constructs
	"""

	# extending symbols
	r_atsign		= r'[@]'

	def __init__(self, *args, **kwargs):
		super(DungeonTalk, self).__init__(*args, **kwargs)

		DungeonTalk.bind_keyword('WAIT', DungeonTalk.Wait)
		DungeonTalk.bind_keyword('GO', DungeonTalk.Go)

		DungeonTalk.bind_symbol(DungeonTalk.r_atsign, {
			Lang.r_identifier:	Lang.handler(DungeonTalk.Character),
			None: 				Lang.handler(DungeonTalk.Ego)
		})

		DungeonTalk.bind_keyword('EYES_ONLY', DungeonTalk.EyesOnly)
		DungeonTalk.bind_keyword('UNTIL', DungeonTalk.Until)
		
		#DungeonTalk.bind_keyword('BY', DungeonTalk.By)
		#DungeonTalk.bind_keyword('TUNE', DungeonTalk.Tune)


	# entity

	class Character(Lang.Identifier):
			
		def __repr__(self):
			return '<character>'

	class Ego(Character):
		pass

	
	class Until(Lang.Parameter):
				
		def __init__(self, *args, **kwargs):
			super(DungeonTalk.Until, self).__init__(*args, **kwargs)
		
	"""	
	class By(Lang.Parameter):
		
		def __init__(self, *args, **kwargs):
			super(DungeonTalk.By, self).__init__(*args, **kwargs)
		
	
	class Tune(Lang.Parameter):
		
		def __init__(self, *args, **kwargs):
			super(DungeonTalk.Tune, self).__init__(*args, **kwargs)
	"""

	class EyesOnly(Lang.Keyword):

		def type(self):
			return '<eyes-only>'
		
		def parse(self, parser, **kwargs):
			
			self.readers = parser.build(parser.expression())

			return [self, self.readers]

			#self.condition	= parser.build(parser.expression())
			#self.until		= parser.build(parser.clause(DungeonTalk.Until))
			#return [self, self.condition, self.until]
		
		def eval(self, interp, expression):
			print 'EYES ONLY %s' % (self.readers)
		
	class Wait(Lang.Keyword):
		
		def type(self):
			return '<wait>'
		
		def parse(self, parser, **kwargs):
			self.condition	= parser.build(parser.expression())
			self.until		= parser.build(parser.clause(DungeonTalk.Until))
			return [self, self.condition, self.until]
		
		def eval(self, interp, expression):
			c = interp.eval(self.condition)
			u = interp.eval(self.until)
			print "WAITING %s UNTIL %s" % (c, u)

	class Go(Lang.Keyword):
		
		def type(self):
			return '<go>'
		
		def parse(self, parser, **kwargs):
			self.destination	= parser.build(parser.expression())
			return [self, self.destination]
		
		def eval(self, interp, expression):
			d = interp.eval(self.destination)
			print "GO %s" % (d)

			print interp


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
			super(DungeonTalk.Tailed, self).__init__(token,pos, **kwargs)	
	"""