"""
	** Aamod Kore **
	Computer Science and Engineering,
	Indian Institute of Technology - Bombay.
	www.cse.iitb.ac.in/~aamod
	aamod[at]cse.iitb.ac.in
"""


"""
Code generates data files (.rd files) for randomly generated test cases.
The results are of the form :
<i> <request r_i> <server config c_i> <> <d(i)> <SUM (j=0 to i) d(j)> <a(i)> <SUM (j=0 to i) a(j)>

The last line contains of the file contains:
<D = SUM (j=0 to N) d(j)> <A = SUM (j=0 to N) a(j)> <Terminal Sum = T>

Read the README file within the data folder for more details

"""


import random
import sys

import WorkFunction
from WorkFunction import *

perim = 36
tests = 10

"""Distaance function of the circle metric"""		
def c_metric(a,b) :
	a = 0 if not a else a%perim
	b = 0 if not b else b%perim
	d = (b-a)%perim
	if d > perim//2 :
		return perim-d
	return d

"""Finding midpoint of an arc on the circle"""
def c_metric_mid(a,b) :
	a = 0 if not a else a%perim
	b = 0 if not b else b%perim
	if a==b :
		return (a+perim//2)%perim
	d = (b-a)%perim
	return (a+d//2)%perim

def vector(r,k):
	return k*[r]

"""Finding farthest (diametrically opposite) point on circle"""
def c_metric_opp(a) :
	return (a+perim//2)%perim

"""Generate reqquest"""
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
	print("begin? ", end="")
	b = int(input())

	for t in range(5) :
		b += 1
		filename = "case" + ("%03d" % b) + ".rd"
		fp = open(filename, 'w')

		initial = random.sample(range(perim), 3)
		# initConfig = (0,0,0)
		initConfig = tuple(initial)
		wf = WorkFunction(list(initConfig), c_metric)

		# print("Initial config:", end=" ")
		# for q in range(len(initial)) :
		# 	print(initial[q], end=" ")

		cost = wf.value(0, wf.config)
		terminalSum = vector(cost,3)
		print(perim, file=fp)
		print(initConfig, file=fp)
		i = 0
		onlineCost = 0
		sumDiff = 0
		sumDiffOpp = 0
		while i < tests :
			mid = generate(wf.config)
			next = (mid+1)%perim
			while True :
				if mid not in wf.config :
					wf.add_request(mid)
				elif next not in wf.config :
					wf.add_request(next)
				else :
					break
				i += 1
				prevConfig = tuple(wf.config)
				cost = wf.process_request(i)
				# Calculate OPT(i+1,c_i)-OPT(i,c_i)
				complementVec = vector(c_metric_opp(wf.requests[i-1]),3)
				diff = wf.value(i,list(prevConfig)) - wf.value(i-1,list(prevConfig))
				sumDiff += diff 
				# Calculate OPT(i+1,r'_i^k)-OPT(i,r'_i^k)
				diffOpp = wf.value(i,complementVec) - wf.value(i-1,complementVec)
				sumDiffOpp += diffOpp 
				print(i, wf.config, cost[0], diff, sumDiff, diffOpp, sumDiffOpp, file=fp)
				onlineCost += cost[0]
				terminalSum[cost[1]] = wf.value(i,wf.config)
				# print("Done: %d %s"%(i,mid), file=sys.stderr)
				# print(i, wf.requests[i-1], cost[1])

		print(sumDiff, sumDiffOpp, sum(terminalSum), file=fp)
		# print(b, perim, i, sumDiff, sumDiffOpp, sum(terminalSum), file=sys.stderr)
		del wf.stored

		opt = ServerSpace(c_metric)
		opt.add_servers(list(initConfig))
		optPath = opt.process_requests(wf.requests)
		optCost = optPath[0]

		print("\nOptimal :", file=fp)
		for p in range(3) :
			rlist = optPath[1][p][1]
			print("Server %d : "%p, file=fp)
			for q in range(len(rlist)) :
				print(optPath[1][p][1][q], end=" ", file=fp)
			print(file=fp)

		fp.close()
		print("Done", t)
		print("%3d %4d %7d %7d\t%2.3f"%(perim, tests, onlineCost, optCost, onlineCost/optCost), file=sys.stderr)

		
