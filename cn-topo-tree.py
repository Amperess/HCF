"""Tree topology"""
from mininet.topo import Topo

class MyTopo( Topo ):
	def __init__(self):
		Topo.__init__(self)

		q1 = []
		q2 = []
		ip = 127
		switch = self.addSwitch("s"+str(ip))
		q1.append((switch, 0, 255))

		depth = 1
		while depth < 4:
			while len(q1) > 0:
				parent = q1.pop(0)
				pSwitch = parent[0]
				lip = parent[1]
				rip = parent[2]
				lSwitch = self.addSwitch("s"+str(self.findMiddle(lip, self.findMiddle(lip,rip))))
				rSwitch = self.addSwitch("s"+str(self.findMiddle(self.findMiddle(lip,rip), rip)))
				

				self.addLink(lSwitch, pSwitch)
				self.addLink(rSwitch, pSwitch)

				q2.append((lSwitch, lip, self.findMiddle(lip, rip)))
				q2.append((rSwitch, self.findMiddle(lip, rip), rip))
				
			q1 = q2
			q2 = []
			depth+=1
		while len(q2) > 0:
			parent = q1.pop[0]
			pSwitch = parent[0]
			lip = parent[1]
			rip = parent[2]


	def findMiddle(self, a, b):
		return (b-a)/2+a
topos = { 'mytopo' : (lambda: MyTopo())}			
			
