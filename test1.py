import random
import sys

import WorkFunction
from WorkFunction import *

perim = 180
tests = 1000
		
def c_metric(a,b) :
	a = 0 if not a else a%perim
	b = 0 if not b else b%perim
	d = (b-a)%perim
	if d > 45 :
		return perim-d
	return d

def c_metric_mid(a,b) :
	a = 0 if not a else a%perim
	b = 0 if not b else b%perim
	if a==b :
		return a
	d = (b-a)%perim
	return a+d//2


def generate(conf) :
	n = len(conf)
	config = sorted(conf)
	maximum, ans = 0, 0
	for i in range(n) :
		j = 0 if i==n-1 else i+1
		mid = c_metric_mid(config[i], config[j])
		dist = c_metric(config[i], mid)
		# print(config[i], config[j], mid, dist)
		if dist > maximum :
			maximum, ans = dist, mid
	return ans


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

	for t in range(1) :
		initial = random.sample(range(perim), 3)
		wf = WorkFunction(initial, c_metric)

		onlineCost = 0
		for i in range(tests) :
			mid = generate(wf.config)
			wf.add_request(mid)
			cost = wf.process_request(i+1)
			onlineCost += cost[0]
			print("Done: %d %s"%(i,mid), file=sys.stderr)

		opt = ServerSpace(c_metric)
		opt.add_servers(initial)
		optCost = (opt.process_requests(wf.requests))[0]

		print("%3d %4d %7d %7d\t%2.3f"%(perim, tests, onlineCost, optCost, onlineCost/optCost))
