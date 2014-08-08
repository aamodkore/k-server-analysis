"""
	** Aamod Kore **
	Computer Science and Engineering,
	Indian Institute of Technology - Bombay.
	www.cse.iitb.ac.in/~aamod
	aamod[at]cse.iitb.ac.in
"""

import random
import sys

import WorkFunction
from WorkFunction import *

perim = 100
tests = 100
		
def c_metric(a,b) :
	a = 0 if not a else a%perim
	b = 0 if not b else b%perim
	d = (b-a)%perim
	if d > perim//2 :
		return perim-d
	return d

def c_metric_mid(a,b) :
	a = 0 if not a else a%perim
	b = 0 if not b else b%perim
	if a==b :
		return (a+perim//2)%perim
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
	
	for t in range(10) :
		initial = random.sample(range(perim), 3)
		# initConfig = (0,0,0)
		initConfig = tuple(initial)
		wf = WorkFunction(list(initConfig), c_metric)

		# print("Initial config:", end=" ")
		# for q in range(len(initial)) :
		# 	print(initial[q], end=" ")

		onlineCost = 0
		for i in range(tests) :
			mid = random.randrange(perim)
			wf.add_request(mid)
			cost = wf.process_request(i+1)
			onlineCost += cost[0]
			# print("Done: %d %s"%(i,mid), file=sys.stderr)
			print(i, mid, cost[1])

		opt = ServerSpace(c_metric)
		opt.add_servers(list(initConfig))
		optPath = opt.process_requests(wf.requests)
		optCost = optPath[0]

		print("\nOptimal :")
		for p in range(3) :
			rlist = optPath[1][p][1]
			print("Server %d : "%p)
			for q in range(len(rlist)) :
				print(optPath[1][p][1][q], end=" ")
			print()
		
		print("%3d %4d %7d %7d\t%2.3f"%(perim, tests, onlineCost, optCost, onlineCost/optCost), file=sys.stderr)
