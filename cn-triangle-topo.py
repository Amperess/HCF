from mininet.topo import Topo

class MyTopo(Topo):
	def __init__(self):
		#Initialize topology
		Topo.__init__(self)

		# Add hosts and switches
		host1 = self.addHost('h1')
		host2 = self.addHost('h2')
		host3 = self.addHost('h3')

		# Add switches
		switch = self.addSwitch('s1')

		# Add links
		self.addLink(host1, switch)
		self.addLink(host2, switch)
		self.addLink(host3, switch)
		
topos = { 'mytopo': (lambda: MyTopo() ) }
