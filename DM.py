from dungeontalk.core.interp import Interpreter
from dungeontalk import DungeonTalk
from dungeon import Dungeon, Room, Route
from character import Character

class DM(Interpreter):
	lang = DungeonTalk()

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

		
		self.cast = []

		self.cast.append(Character())

		print self.cast
		"""
		import pip
		installed_packages = pip.get_installed_distributions()
		installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
		print(installed_packages_list)
		"""

	
	def test(self):
		routes = self.city.get_path('Bar', 'Safehouse');


		for r in routes[0]:
			print r

		#for r in routes:
		#	print r.get_length()
	
		#print self.city.get_vertex('Train Station').get_outbound_edges()


	def __init__(self, *args, **kwargs):
		
		super(DM, self).__init__(*args, **kwargs)

		self.init_world()
		self.init_cast()
	