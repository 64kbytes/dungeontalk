from copy import copy, deepcopy
import exc

class Vertex(object):

	def set_graph(self, graph):
		self.graph = graph
		return self

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
		return [(edge, edge.get_head()) for id,edge in self.outbound.items()]

	def __init__(self, identifier=None):
		self.undirected = {}
		self.inbound 	= {}
		self.outbound 	= {}
		self.id = identifier or id(self)

	def __repr__(self):
		return '<%s, %s>' % (self.id, self.graph)


class Edge(object):

	@staticmethod
	def invert(edge):
		iedge = deepcopy(edge)
		return iedge.set_tail(edge.get_head()).set_head(edge.get_tail())

	def get_id(self):
		return self.id

	def set_tail(self, vertex):
		self.tail = vertex
		return self

	def set_head(self, vertex):
		self.head = vertex
		return self

	def set_weight(self, weight):
		self.weight = weight
		return self

	def get_head(self):
		return self.head

	def get_tail(self):
		return self.tail

	def get_vertices(self):
		return self.tail, self.head
	
	def get_weight(self):
		return self.weight or 1

	def __init__(self, identifier=None, tail=None, head=None, weight=None, is_directed=True):
		self.id = identifier or id(self)
		self.is_directed = is_directed
		self.set_tail(tail)
		self.set_head(head)
		self.set_weight(weight)

	def __repr__(self):
		return '<(%s)%s-%s>' % ('d' if self.is_directed else 'u', self.tail.id, self.head.id)


class Path(object):

	def get_length(self):
		return sum([edge.get_weight() for edge in self.edges])
		
	def __init__(self, edges=[]):
		self.edges = edges
		self.i = 0

	def __iter__(self):
		return self

	def next(self):
		if self.i < len(self.edges):
			i = self.i
			self.i += 1
			return self.edges[i]
		else:
			raise StopIteration()

	def __repr__(self):
		return "<path %s>" % (','.join([str(edge) for edge in self.edges]))
		

class MultiDigraph(object):

	def add_vertex(self, vertex):
		vertex.set_graph(self)
		self.vertices[vertex.get_id()] = vertex
		return self

	def add_vertices(self, vertices):

		for v in vertices if isinstance(vertices, list) else [vertices]:
			self.add_vertex(v)

		return self

	def get_vertices(self, id_list=[]):
		
		if len(id_list) > 0:
			return [self.get_vertex(id) for id in id_list]

		return self.vertices

	def get_vertex(self, identifier):
		v = self.vertices.get(identifier, None)

		if v is None:
			raise exc.VertexNotFound("'%s' not found" % (identifier));

		return v

	def get_adjacency_matrix(self):
		return self.adjacency_matrix

	def compute_adjacency_matrix(self):
		return {vertex.get_id(): vertex.get_neighbours() for id, vertex in self.get_vertices().items()}

	def update_adjacency_matrix(self):
		self.adjacency_matrix = self.compute_adjacency_matrix()

	def _find_path(self, begin, end, _from_edge=None, _path=[]):
		"""
		Search depth-first recursively all paths leading from start to to end
		Kind of messy. Can be improved
		"""

		# accept vertices or IDs
		if isinstance(begin, Vertex):
			begin = begin.get_id()

		if isinstance(end, Vertex):
			end = end.get_id()

		routes 		= []
		path 		= copy(_path)
		from_edge 	= copy(_from_edge)
		path.append((from_edge, begin))
		
		for (edge, vertex) in [(edge, vertex.get_id()) for (edge, vertex) in self.adjacency_matrix[begin] if vertex.get_id() not in [p for e,p in path]]:

			if vertex == end:
				path.append((edge, end))
				return [Path(edges=[e for e,v in path if e is not None])] 

			solution_path = self._find_path(vertex, end, edge, path)

			if len(solution_path) > 0:
				routes.append(solution_path)

		return routes

	def _unnest(self, haystack, needle):

		if not isinstance(haystack, list):
			raise TypeError()

		paths = []

		while(haystack):

			current = haystack.pop()

			if isinstance(current, needle):
				paths.append(current)
			else:
				for i in current:
					haystack.append(i)

		return paths

	def get_path(self, begin, end):
		return self._unnest(self._find_path(begin, end), Path)


	def connect(self, tail, head, edge):

		edge.set_tail(tail)
		edge.set_head(head)
		
		if edge.is_directed:
			tail.add_outbound_edge(edge)
			head.add_inbound_edge(edge)
		else:
			tail.add_undirected_edge(edge)
			head.add_undirected_edge(Edge.invert(edge))

		self.add_vertices([tail, head])

	def __init__(self, vertices=[]):
		self.vertices = {}
		self.add_vertices(vertices)

		



"""
def breadth_first_search(self):
	if not isinstance(begin, Vertex):
		begin = self.get_vertex(begin)

	expand 	= [begin]
	visited = {begin.get_id(): True}
	path 	= [begin]
	path 	= []
	routes 	= []
	
	while(len(expand) > 0):

		current = self.get_vertex(expand.pop().get_id())

		path.append(current)

		if current.get_id() == end:
			routes.append(path)
			path = []
			expand = [begin]
			continue
		
		for vertex in current.get_neighbours():

			if visited.get(vertex.get_id(), None) is None:
				expand.append(vertex)
				visited[vertex.get_id()] = True


	print routes
"""