from core import Phase

class Planning(Phase):
	def begin(self):
		print '\nTURN %s' % (self.dm.get_turn())
		print '-'*80
	
	def listen(self, instruction):
	
		if instruction == 'end turn':
			self.end()
			return '+'
		else:
			self.dm.ego.set_instruction(instruction)

		return 'Ok'
		
	def end(self):
		super(Planning, self).end()


class Execution(Phase):
	def begin(self):
		print "Ok, let's go...\n"

		print 'Roll initiative...'
		initiative_rolls = self.dm.roll_initiative()

		for character,roll in initiative_rolls:
			print "%s got %s" % (character.get_full_name(), roll)

		print '\nCharacters do...\n'

		for character,roll in initiative_rolls:
			print "%s %s" % (character.get_full_name(), character.get_instructions() or 'Do nothing')
			
			

			#self.dm.read(character.get_instructions())
			#self.dm.load()
			#print self.dm.get_next_instruction()
			#self.dm.clear()

		self.end()

	def end(self):
		super(Execution, self).end()


class Adjust(Phase):
	def begin(self):
		self.end()

	def end(self):
		super(Adjust, self).end()


class Review(Phase):
	
	def begin(self):
		self.end()

	def end(self):
		super(Review, self).end()