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

		self.connect(bar, train_station, Route(is_directed=False))
		self.connect(train_station, brandenburg_gate, Route(is_directed=False))
		self.connect(train_station, underground, Route(is_directed=True))#
		
		self.connect(underground, depot, Route(is_directed=True))#
		self.connect(depot, docks, Route(is_directed=False))
		self.connect(depot, waterworks, Route(is_directed=True))#
		self.connect(docks, autobahn, Route(is_directed=False))

		self.connect(autobahn, airport, Route(is_directed=False))
		self.connect(autobahn, brandenburg_gate, Route(is_directed=False))
		
		self.connect(brandenburg_gate, embassy, Route(is_directed=False))
		self.connect(brandenburg_gate, park, Route(is_directed=False))
		
		self.connect(park, hotel, Route(is_directed=False))
		self.connect(park, dark_alley, Route(is_directed=False))
		self.connect(dark_alley, safehouse, Route(is_directed=False))

		self.connect(safehouse, waterworks, Route(is_directed=True))#
		self.connect(waterworks, park, Route(is_directed=True))#

		self.update_adjacency_matrix()

		print self.adjacency_matrix
		print 80*'-'


