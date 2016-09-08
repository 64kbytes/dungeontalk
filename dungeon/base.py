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