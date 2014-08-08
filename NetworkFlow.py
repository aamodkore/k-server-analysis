"""
	** Aamod Kore **
	Computer Science and Engineering,
	Indian Institute of Technology - Bombay.
	www.cse.iitb.ac.in/~aamod
	aamod[at]cse.iitb.ac.in
"""

import queue

"""A large real number"""
LRN = 999999
"""An even larger infinity"""
infinity = 9999999999999

class Edge(object):
	"""Class for directed edge in graph"""
	def __init__(self, u, v, cp, cs):
		self.source = u
		self.sink = v  
		self.capacity = cp
		self.cost = cs
		"""redge stores the reverse edge 
		from the sink to source"""
		self.redge = None
	def __repr__(self):
		return "%s->%s:%s:%s" % (self.source, self.sink, self.capacity, self.cost)

 
class FlowNetwork(object):
	"""Class for the graph of the network"""
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

	"""Adding an edge also adds its reverse edge.
	Thus in all there may be 4 edges between 2 vertices."""
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

	"""Using Bellman-Ford Algorithm to calculate 
				non-negative vertex potentials. """
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

	"""Calculate least cat path using Bellman-Ford algorithm"""
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


	"""Reduce edge costs to non-negative values,without 
				altering possible least-cost paths"""
	def reduce_costs(self) :
		for u in self.vertices :
			for edge in self.adj[u] :
				residual = edge.capacity - self.flow[edge]
				if residual > 0 : 
					v = edge.sink 
					edge.cost = edge.cost + self.distance[u] - self.distance[v]
					edge.redge.cost = 0

	
	"""Find least cost path using Djikstra's Algorithm 
				(assumes non-negative edge costs)"""
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

 
	"""Find Minimum cost maximum flow using repeated edge relaxation
				along least cost path, found using
				Belmann-Ford algorithm"""
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


	"""Find Minimum cost maximum flow using repeated edge relaxation
				along least cost path, found using
				reduced edge costs and reduced vertex 
				potentials found by Belmann-Ford algorithm
		For more details refer:
	http://community.topcoder.com/tc?module=Static&d1=tutorials&d2=minimumCostFlow2"""
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
	"""Stores the metric space for the servers and the
				initial server positions"""
	def __init__(self, m):
		self.servers = []
		self.metric = m
	
	"""Adds a server given the initial position of the server"""
	def add_server(self, pos) :
		self.servers.append(pos)

	"""For each member in the list provided, adds a server at the
				corrosponding initial position"""
	def add_servers(self,poslist) :
		self.servers += poslist

	"""Computes offline the optimal cost for processing a given
				sequence of requests.
		For complete algorithm refer :
		M Chrobak, H Karloff, T Payne, S Vishwanathan: New Results on Server Problems"""
	def process_requests(self, requests) :
		
		"""Maps(dictionary maps) to store nodes in the
			graph corresponding to servers and requests"""
		snode = {}
		rnode = {}
		ventity = {}
		v = 1
		ns = len(self.servers)
		nr = len(requests)
		n = ns + 2*nr + 1
		
		"""Create the corresponding flow network graph"""
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
		
		"""Calculate min-cost max flow in the graph"""
		k = graph.min_cost_max_flow(0,n)
		if k != ns :
			print(graph)
			raise RuntimeError("Something went wrong: k=%s, ns=%s " % (k,ns))

		"""Evaluate total cost and sequence in which the 
				servers process the requests"""
		process = [] 
		totalCost = 0
		for s in range(ns) :
			v = snode[s] 
			rlist = []
			while v != n :
				if v > 0 and v <= 2*nr and v%2:
					r = ventity[v]
					if len(rlist)==0 :
						totalCost += self.metric(self.servers[s], requests[r])
					else :
						totalCost += self.metric(requests[rlist[-1]], requests[r])
					rlist.append(r)
				for edge in graph.get_edges(v) :
					if graph.get_flow(edge) > 0 :
						v = edge.sink
						break
			process.append((s, rlist))
		del graph
		return (totalCost, process)


if __name__=="__main__" :
	"""Test case. Duh!"""
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

	ss.add_servers([(5,0), None, None])
	a = None
	b = (1,0)
	c = (12,0)
	d = (13,0)

	print(ss.process_requests([a,b,c,d,c,d,a,b,a,b]))
