class Knowledge(object):
	
	def __iter__(self):
		return self

	def next(self):
		if self.i < len(self.knowledge):
			i = self.i
			self.i += 1
			return self.facts[i]
		else:
			raise StopIteration()

	def record(self, knowledge):
		self.knowledge.append(knowledge)

	def __init__(self, *args, **kwargs):
		self.knowledge = []
		self.i = 0

	def __repr__(self):
		return str(self.knowledge)