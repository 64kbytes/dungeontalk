from dungeontalk.core.interp import Interpreter
from dungeontalk import DungeonTalk
from dungeon import Dungeon

class DM(Interpreter):
	lang = DungeonTalk()

	def __init__(self, *args, **kwargs):
		super(DM, self).__init__(*args, **kwargs)

		self.city = Dungeon()

	def test(self):
		routes = self.city.get_path('Bar', 'Safehouse');

		print routes

		print routes[0].get_length()

		#print self.city.get_vertex('Train Station').get_outbound_edges()