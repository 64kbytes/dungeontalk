from dungeontalk.core.interp import Interpreter
from dungeontalk import DungeonTalk
from dungeon import Dungeon

class DM(Interpreter):
	lang = DungeonTalk()

	def __init__(self, *args, **kwargs):
		super(DM, self).__init__(*args, **kwargs)

		self.city = Dungeon()

	def test(self):
		print self.city.get_path('Bar', 'Airport')