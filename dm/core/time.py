class Turn(object):

	def __iter__(self):
		return self

	def next(self):

		if self.phasenum < len(self.phases)-1:
			self.phasenum += 1
		else:
			self.turn += 1
			self.phasenum = 0

		self.dm.set_running_phase(self.get_running_phase())
		return self.get_running_phase()

	
	def get_turn(self):
		return self.turn

	def get_running_phase(self):
		return self.phases[self.phasenum]

	def begin_cycle(self):
		assert self.phasenum == -1, "Begin cycle should be call'd only once to start turn cycling"
		self.next().begin()
		return self

	def end_phase(self):
		self.next().begin()
		return self

	def add_phases(self, phases):
		
		if not isinstance(phases, list):
			phases = [phases]

		for p in phases:
			self.phases.append(p(dm=self.dm, turn=self))

		return self

	def __init__(self, dm=None, phases=[]):
		self.phasenum 	= -1 # phase cycle starts with phasenum++, so...
		self.turn 		= 0
		self.dm 		= dm
		self.phases 	= []
		self.add_phases(phases)

	def __repr__(self):
		return str(self.phases)

class Phase(object):

	def __init__(self, dm, turn):
		self.dm = dm
		self.turn = turn

	def begin(self):
		pass
	
	def listen(self):
		pass

	def end(self):
		self.turn.end_phase()