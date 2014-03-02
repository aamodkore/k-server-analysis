import queue

LRN = 999999
infinity = 9999999999999
class Edge(object):
	def __init__(self, u, v, cp, cs):
		self.source = u
		self.sink = v  
		self.capacity = cp
		self.cost = cs
		self.redge = None
	def __repr__(self):
		return "%s->%s:%s:%s" % (self.source, self.sink, self.capacity, self.cost)

 
class FlowNetwork(object):
	def __init__(self):
		self.adj = {}
		self.distance = {}
		self.flow = {}
		self.vertices = set([])

	def __repr__(self):
		st = ""
		for u in self.vertices :
			st += "[v::%s, adj::[ " % (u)
			for edge in self.adj[u] :
				if edge.capacity > 0 :
					st += "(%s ::f:%s) " %  (edge, self.flow[edge])
			st += "]]\n"
		return st
 
	def add_vertex(self, vertex):
		self.distance[vertex] = infinity
		self.adj[vertex] = []
		self.vertices.add(vertex)
 
	def get_edges(self, v):
		return self.adj[v]
 
	def get_flow(self, edge) :
		return self.flow[edge]

	def add_edge(self, u, v, w=0, c=1):
		if u == v:
			raise ValueError("u == v")
		edge = Edge(u,v,w,c)
		redge = Edge(v,u,0,c*-1)
		edge.redge = redge
		redge.redge = edge
		self.adj[u].append(edge)
		self.adj[v].append(redge)
		self.flow[edge] = 0
		self.flow[redge] = 0

	def bellman_ford_potentials(self, source) :
		for u in self.vertices :
			self.distance[u] = infinity
		self.distance[source] = 0
		for ix in range(len(self.vertices)) :
			acc = 0
			for u in self.vertices :
				for edge in self.adj[u] :
					residual = edge.capacity - self.flow[edge]
					if residual > 0 :
						v = edge.sink
						if self.distance[u] + edge.cost < self.distance[v] :
							self.distance[v] = self.distance[u] + edge.cost
							acc = acc + 1
			if acc == 0 :
				break

	def bellman_ford_path(self, source, sink) :
		predecessor = {}
		for u in self.vertices :
			predecessor[u] = None
			self.distance[u] = infinity
		self.distance[source] = 0
		for ix in range(len(self.vertices)) :
			acc = 0
			for u in self.vertices :
				for edge in self.adj[u] :
					residual = edge.capacity - self.flow[edge]
					if residual > 0 :
						v = edge.sink
						if self.distance[u] + edge.cost < self.distance[v] :
							self.distance[v] = self.distance[u] + edge.cost
							predecessor[v] = edge
							acc = acc + 1
			if acc == 0 :
				break
		u = predecessor[sink]
		result = []
		while u != None and len(result) <= len(self.vertices) :
			result = [u] + result
			if u.source == source :
				return result
			u = predecessor[u.source]
		return None


	def reduce_costs(self) :
		for u in self.vertices :
			for edge in self.adj[u] :
				residual = edge.capacity - self.flow[edge]
				if residual > 0 : 
					v = edge.sink 
					edge.cost = edge.cost + self.distance[u] - self.distance[v]
					edge.redge.cost = 0

	def find_path(self, source, sink):
		openList = set([])
		predecessor = {}
		for u in self.vertices :
			predecessor[u] = None
			d = 0 if u==source else infinity
			self.distance[u] = d
			openList.add((d, u))

		while len(openList) != 0 :
			p, u = min(openList)
			openList.remove((p,u))
			for edge in self.adj[u] :
				v = edge.sink
				d = p + edge.cost
				residual = edge.capacity - self.flow[edge]
				if residual > 0 and self.distance[v] > d and (self.distance[v],v) in openList:
					openList.remove((self.distance[v], v))
					self.distance[v] = p + edge.cost
					predecessor[v] = edge
					openList.add((self.distance[v], v))
		
		u = predecessor[sink]
		result = []
		while u != None and len(result) <= len(self.vertices) :
			result = [u] + result
			if u.source == source :
				return result
			u = predecessor[u.source]

		return None

 
	def max_flow(self, source, sink):
		path = self.bellman_ford_path(source, sink)
		while path != None:
			residuals = [edge.capacity - self.flow[edge] for edge in path]
			flow = min(residuals)
			for edge in path:
				self.flow[edge] += flow
				self.flow[edge.redge] -= flow
			path = self.bellman_ford_path(source, sink)
		return sum(self.flow[edge] for edge in self.get_edges(source))


	def min_cost_max_flow(self, source, sink):
		self.bellman_ford_potentials(source)
		self.reduce_costs()
		path = self.find_path(source, sink)
		while path != None:
			# print("Path is: ", path)
			self.reduce_costs()
			residuals = [edge.capacity - self.flow[edge] for edge in path]
			flow = min(residuals)
			for edge in path:
				self.flow[edge] += flow
				self.flow[edge.redge] -= flow
			path = self.find_path(source, sink)
		return sum(self.flow[edge] for edge in self.get_edges(source))


class ServerSpace(object):
	def __init__(self, m):
		self.servers = []
		self.metric = m
	
	def add_server(self, pos) :
		self.servers.append(pos)

	def add_servers(self,poslist) :
		self.servers += poslist

	def process_requests(self, requests) :
		process = [] 
		
		snode = {}
		rnode = {}
		ventity = {}
		v = 1
		ns = len(self.servers)
		nr = len(requests)
		n = ns + 2*nr + 1
		graph = FlowNetwork()
		
		graph.add_vertex(0)
		ventity[0] = 0
		graph.add_vertex(n)
		for r in range(nr) :
			graph.add_vertex(v)
			graph.add_vertex(v+1)
			for j in rnode.keys() :
				dist = self.metric(requests[j],requests[r])
				graph.add_edge(rnode[j]+1,v,1,dist)
			graph.add_edge(v+1,n,1,0)
			graph.add_edge(v,v+1,1,-LRN)
			rnode[r] = v
			ventity[v] = ventity[v+1] = r
			v += 2
		for s in range(ns) :
			graph.add_vertex(v)
			graph.add_edge(0,v,1,0)
			graph.add_edge(v,n,1,0)
			for r in range(nr) :
				dist = self.metric(self.servers[s],requests[r])
				graph.add_edge(v,rnode[r],1,dist)
			ventity[v] = s
			snode[s] = v
			v += 1
		k = graph.min_cost_max_flow(0,n)
		if k != ns :
			print(graph)
			raise RuntimeError("Something went wrong: k=%s, ns=%s " % (k,ns))

		for s in range(ns) :
			v = snode[s] 
			rlist = []
			while v != n :
				if v > 0 and v <= 2*nr and v%2:
					rlist.append(ventity[v])
				for edge in graph.get_edges(v) :
					if graph.get_flow(edge) > 0 :
						v = edge.sink
						break
			process.append((s, rlist))

		return process

if False :
	g = FlowNetwork()

	# [g.add_vertex(v) for v in "sopqrt"]

	# g.add_edge('s','o',3)
	# g.add_edge('s','p',3)
	# g.add_edge('o','p',2)
	# g.add_edge('o','q',3)
	# g.add_edge('p','r',2)
	# g.add_edge('r','t',3)
	# g.add_edge('q','r',4)
	# g.add_edge('q','t',2)

	########## EX - 2 ################
	# [g.add_vertex(v) for v in "s12345t"]
	# g.add_edge('s','1',5, 0)
	# g.add_edge('1','2',7, 1)
	# g.add_edge('1','3',7, 5)
	# g.add_edge('2','3',2,-2)
	# g.add_edge('2','4',3, 8)
	# g.add_edge('3','4',3,-3)
	# g.add_edge('3','5',2, 4)
	# g.add_edge('4','t',3, 0)
	# g.add_edge('5','t',2, 0)

	##################################
	print(g.min_cost_max_flow('s','t'))
	print(g)

def metric(a,b) :
	if a == None :
		if b == None :
			return 0
		else :
			return metric(b,a)
	if b != None :
		return metric((a[0]-b[0],a[1]-b[1]),None)
	else :
		return -a[0] if (a[0]<0) else a[0]

ss = ServerSpace(metric)

ss.add_servers([None, None, None])
a = None
b = (1,0)
c = (12,0)
d = (13,0)

print(ss.process_requests([a,b,c,d,c,d,a,b,a,b]))
