class Vertex(object):

	def get_id(self):
		return self.id

	def add_inbound_edge(self, edge):
		self.inbound[edge.id] = edge

	def add_outbound_edge(self, edge):
		self.outbound[edge.id] = edge

	def add_undirected_edge(self, edge):
		self.add_inbound_edge(edge)
		self.add_outbound_edge(edge)

	def get_inbound_edges(self):
		return self.inbound

	def get_outbound_edges(self):
		return self.outbound

	def get_neighbours(self):
		edges = self.inbound.copy()
		edges.update(self.outbound)

		

		#return [dict(t) for t in set([tuple(v) for k,v in edges.items()])]

		#return [dict(t) for t in set([tuple(edges.items())])]

	def __init__(self, identifier=None):
		self.undirected = {}
		self.inbound 	= {}
		self.outbound 	= {}
		self.id = identifier or id(self)

	def __repr__(self):
		return '<%s>' % (self.id)


class Edge(object):

	def get_id(self):
		return self.id

	def set_tail(self, vertex):
		self.tail = vertex

	def set_head(self, vertex):
		self.head = vertex

	def set_weight(self, weight):
		self.weight = weight

	def get_head(self):
		return self.head

	def get_tail(self):
		return self.tail

	def get_vertices(self):
		return self.tail, self.head
	
	def __init__(self, identifier=None, tail=None, head=None, weight=None, is_directed=True):
		self.id = identifier or id(self)
		self.is_directed = is_directed
		self.set_tail(tail)
		self.set_head(head)
		self.set_weight(weight)

	def __repr__(self):
		return '<%s-%s>' % (self.tail.id, self.head.id)

class MultiDigraph(object):

	def add_vertex(self, vertex):
		self.vertices[vertex.get_id()] = vertex

	def add_vertices(self, vertices):

		vertices = vertices if isinstance(vertices, list) else [vertices]

		for v in vertices:
			self.add_vertex(v)

	def get_incidence_table(self):

		table = {}

		for id, vertex in self.vertices.items():
			
			print vertex.get_neighbours()

			#neighbours = vertex.get_outbound_edges

	def get_path(self, begin, end, path=[]):

		"""
		if begin != end:
			
			if begin in self.vertices:
				path.append(self.vertices[begin])
		"""

		print self.get_incidence_table()


		return path

	def connect(self, tail, head, edge):

		edge.set_head(head)
		edge.set_tail(tail)

		if edge.is_directed:
			tail.add_outbound_edge(edge)
			head.add_inbound_edge(edge)
		else:
			tail.add_undirected_edge(edge)
			head.add_undirected_edge(edge)

		self.add_vertices([tail, head])

	def __init__(self):
		self.vertices = {}