from dungeontalk.core.interp import Interpreter
from dungeontalk import DungeonTalk
from dungeon import Dungeon, Room, Route
from character import Character
from rand import *
import collections

class DM(Interpreter):
	lang = DungeonTalk()

	class Brief(object):
		def __init__(self, *args, **kwargs):
			for k,v in kwargs.items():
				setattr(self, k, v)

	class Narrator(object):

		def __init__(self, dm):
			self.dm 	= dm
			self.ego 	= dm.get_ego()
			self.room 	= self.ego.get_location()

		def get_brief(self):
			return "%s\n%s\n%s\n" % (self.which_turn(), self.where_is(), self.where_can_go())

		def which_turn(self):
			return "TURN %s\n" % (self.dm.get_turn())

		def where_is(self):
			return "You are in %s." % (self.room.get_id())

		def where_can_go(self):

			exits = [room[1].get_id() for room in self.room.get_neighbours()]
			return "You can go:\n\t%s" % ('\n\t'.join(exits))

	def init_world(self):

		city = Dungeon()

		underground 		= Room('Underground')
		waterworks 			= Room('Waterworks')
		train_station 		= Room('Train Station')
		bar 				= Room('Bar')
		hotel 				= Room('Hotel')
		brandenburg_gate	= Room('Brandenburg Gate')
		embassy 			= Room('Embassy')
		autobahn 			= Room('Autobahn')
		airport 			= Room('Airport')
		park 				= Room('Park')
		docks 				= Room('Docks')
		depot				= Room('Depot')
		dark_alley 			= Room('Dark Alley')
		safehouse 			= Room('Safehouse')

		city.connect(bar, train_station, Route(is_directed=False))
		city.connect(train_station, brandenburg_gate, Route(is_directed=False))
		city.connect(train_station, underground, Route(is_directed=True))#
		
		city.connect(underground, depot, Route(is_directed=True))#
		city.connect(depot, docks, Route(is_directed=False))
		city.connect(depot, waterworks, Route(is_directed=True))#
		city.connect(docks, autobahn, Route(is_directed=False))

		city.connect(autobahn, airport, Route(is_directed=False))
		city.connect(autobahn, brandenburg_gate, Route(is_directed=False))
		
		city.connect(brandenburg_gate, embassy, Route(is_directed=False))
		city.connect(brandenburg_gate, park, Route(is_directed=False))
		
		city.connect(park, hotel, Route(is_directed=False))
		city.connect(park, dark_alley, Route(is_directed=False))
		city.connect(dark_alley, safehouse, Route(is_directed=False))

		city.connect(safehouse, waterworks, Route(is_directed=True))#
		city.connect(waterworks, park, Route(is_directed=True))#

		city.update_adjacency_matrix()

		self.city = city

	def init_cast(self):

		self.cast = [Character(), Character(), Character()]
		self.spawn(self.cast)
		self.ego = choice(self.cast)
		self.ego.set_as_ego()

	def get_turn(self):
		return self.turn

	def get_brief(self):

		narrator = DM.Narrator(dm=self)
		
		return DM.Brief(ego=self.get_ego(), room=self.get_ego().get_location(), description=narrator.get_brief())

	def get_ego(self):
		return self.ego

	def spawn(self, characters):

		for c in characters:
			c.set_location(self.city.get_place(choice([
				'Bar',
				'Train Station',
				'Brandenburg Gate',
				'Autobahn',
				'Park',
				'Waterworks',
				'Underground',
				'Hotel',
				'Embassy',
				'Dark Alley',
				'Docks',
				'Depot',
				'Airport',
				'Safehouse'
			])))

	def instruct_character(self, character, instructions):
		pass

	def roll_initiative(self):
	
		initiative_rolls = []
		for character in self.cast:

			dices = Roll([Dice(20)])
			roll = dices.roll()
			initiative_rolls.append((character, roll))
		
		# sort initiative
		return sorted(initiative_rolls, key=lambda x: x[1], reverse=True)

	def play_turn(self):
		
		print 'Playing turn %s' % (self.turn)
		print '-'*80
		
		print 'Roll initiative...'
		initiative_rolls = self.roll_initiative()

		for character,roll in initiative_rolls:
			print "%s got %s" % (character.get_full_name(), roll)

		print '\nActing...'

		for character,roll in initiative_rolls:

			print character.get_instructions() or 'Do nothing'

		self.end_turn()

	def end_turn(self):
		self.turn += 1

	def welcome(self):
		print 'COLDWAR v0.1'
		print '='*80

	def submit(self, instruction):

		if instruction == 'end turn':
			self.play_turn()
			return '-'*80 + '\n'
		else:
			self.ego.set_instruction(instruction)


	def __init__(self, *args, **kwargs):
		
		super(DM, self).__init__(*args, **kwargs)

		self.turn = 1
		self.init_world()
		self.init_cast()

		self.welcome()

		print 'These are the caracters...'
		for c in self.cast:
			c.get_identity()
		print '-'*80
		print 'Listening for instructions...' + '\n'
	