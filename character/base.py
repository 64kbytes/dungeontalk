from faker import Factory as RandomCharacterFactory
from ai import AI, Automaton, Knowledge

class LocatableMixin(object):
	def set_location(self, room):
		self.location = room
		return self

	def get_location(self):
		return self.location

class Identity(object):
	def __init__(self, randomize=True, is_true=False, **kwargs):

		self.is_true = is_true

		if randomize:
			random = RandomCharacterFactory.create()
			self.first_name 	= random.first_name()
			self.last_name 		= random.last_name()
			self.birth_country 	= random.country()

	def get_full_name(self):
		return "%s %s" % (self.first_name, self.last_name)

class Character(Automaton, LocatableMixin):
	
	def __init__(self, *args, **kwargs):
		
		super(Character, self).__init__(*args, **kwargs)
		
		self.id 		= kwargs.get('id', id(self))
		self.is_ego 	= kwargs.get('is_ego', False)
		self.location 	= None
		self.identity 	= Identity(is_true=True)
		self.inventory 	= []

	def get_id(self):
		return self.id

	def set_as_ego(self):
		self.is_ego = True

	def get_full_name(self):
		return self.identity.get_full_name()

	def get_identity(self):
		# clean this
		id = self.identity
		if self.is_ego:
			print "YOU are %s %s, and you are in %s" % (id.first_name, id.last_name, self.get_location().id)
		else:
			print "%s %s is in %s" % (id.first_name, id.last_name, self.get_location().id) 

	def __repr__(self):
		return self.get_full_name()

		