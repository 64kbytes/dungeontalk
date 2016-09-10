from graph import MultiDigraph, Vertex, Edge

class Room(Vertex):
	
	def __init__(self, *args, **kwargs):
		super(Room, self).__init__(*args, **kwargs) 

		self.characters = []
		self.description = ''

	def set_description(self, description):
		self.description = description
		return self

	def get_description(self):
		return self.description

	def add_entity(self, entity):
		enntity.set_location(self)
		self.characters.append(entity)

class Route(Edge):
	pass

class Dungeon(MultiDigraph):

	def get_place(self, identifier):
		return self.get_vertex(identifier)

	def get_all_places(self, identifier):
		return self.get_vertices()
	
	def __init__(self, *args, **kwargs):
		super(Dungeon, self).__init__(*args, **kwargs)