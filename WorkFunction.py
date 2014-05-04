import NetworkFlow
from NetworkFlow import *		

class WorkFunction(object):
	def __init__(self, init_config, metric):
		self.stored = []
		self.requests = []
		self.config = init_config ;
		self.init_config = init_config ;
		self.metric = metric

	def add_request(self, r) :
		self.requests.append(r)

	def del_request(self) :
		del self.requests[-1]
		if not (len(self.requests)+1 >= len(self.stored)) :
			del self.stored[-1]

	def value(self, t, config) :
		if len(self.requests) < t or t < 0:
			return -1
		while t >= len(self.stored) :
			self.stored.append(dict([]))
		if tuple(config) in self.stored[t] : 
			return (self.stored[t])[tuple(config)]
		# print("Calculating")
		if t==0 :
			(self.stored[t])[tuple(config)] = self.min_cost_to(config)
			return ((self.stored)[t])[tuple(config)]
		n = len(config)
		r = self.requests[t-1]
		minimum = infinity
		for i in range(n):
			temp, config[i] = config[i], r
			val, dist = self.value(t-1, config), self.metric(r, temp)
			if dist == 0:
				(self.stored[t])[tuple(config)] = val 
				return val
			if val+dist < minimum :
				minimum = val+dist
			config[i] = temp
		(self.stored[t])[tuple(config)] = minimum
		return minimum

	def process_request(self, x) :
		if x == -1 :
			x = len(self.requests)
		elif len(self.requests) < x or x <= 0 :
			raise RuntimeError("WorkFunction::process_request : Invalid request index: (x=%d)\n" % x)
		n = len(self.config)
		r = self.requests[x-1]
		minimum = cost = infinity
		for i in range(n):
			temp= self.config[i]
			self.config[i]  = r
			val, dist = self.value(x, self.config), self.metric(r, temp)
			if val+dist < minimum :
				s, cost, minimum = i, dist, val+dist
			self.config[i] = temp
		self.config[s] = r
		return (cost, s)

	def min_cost_to(self, config) :
		n = min(len(config), len(self.init_config))
		graph = FlowNetwork()
		graph.add_vertex(-1)
		graph.add_vertex(-2)

		for i in range(n) :
			graph.add_vertex(i)
			graph.add_vertex(n+i)
			graph.add_edge(-1,i,1,0)
			graph.add_edge(n+i,-2,1,0)

		for i in range(n) :
			for j in range(n) :
				graph.add_edge(i,n+j,1, self.metric(self.init_config[i], config[j]) )
		k = graph.min_cost_max_flow(-1,-2)
		if k != n :
			print(graph)
			raise RuntimeError("Something went wrong: k=%s, ns=%s " % (k,ns))
		cost = 0 
		for i in range(n) :
			for edge in graph.get_edges(i) :
				if graph.get_flow(edge) > 0 :
					cost += edge.cost
					break
		del graph
		return cost


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

	ss = WorkFunction([None, None, None], metric)

	a = None
	b = (12,0)
	c = (12,0)
	d = (13,0)

	rl = [a,b,c,d,c,d,a,b,a,b]
	for i in range(len(rl)) :
		ss.add_request(rl[i])
		print(ss.process_request(i+1))
