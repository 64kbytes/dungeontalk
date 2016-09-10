from faker import Factory as RandomCharacterFactory

class Identity(object):
	def __init__(self, randomize=True, is_true=False):

		self.is_true = is_true

		if randomize:
			random = RandomCharacterFactory.create()
			self.first_name = random.first_name()
			self.last_name 	= random.last_name()

	def get_full_name(self):
		return "%s %s" % (self.first_name, self.last_name)

class Character(object):
	
	def __init__(self):
		self.identity = Identity(is_true=True)

	def __repr__(self):
		return self.identity.get_full_name()

		