from graph import MultiDigraph, Vertex, Edge

class Room(Vertex):
	pass

class Route(Edge):
	pass

class Dungeon(MultiDigraph):

	def get_places(self):
		return self.vertices
	

	def __init__(self, *args, **kwargs):

		super(Dungeon, self).__init__(*args, **kwargs)

		train_station 		= Room('Train Station')
		bar 				= Room('Bar')
		hotel 				= Room('Hotel')
		brandenburg_gate	= Room('Brandenburg Gate')
		embassy 			= Room('Embassy')
		airport 			= Room('Airport')

		self.connect(train_station, bar, Route(is_directed=False))
		self.connect(train_station, airport, Route(is_directed=False))
		self.connect(train_station, brandenburg_gate, Route(is_directed=False))

		self.connect(brandenburg_gate, embassy, Route(is_directed=False))
		self.connect(brandenburg_gate, airport, Route(is_directed=False))
		self.connect(brandenburg_gate, bar, Route(is_directed=False))


