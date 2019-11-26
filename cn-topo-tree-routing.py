"""Tree topology"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

class MyTopo( Topo ):

	def build( self, **_opts ):
		r0 = self.addNode( 'r0', cls=LinuxRouter, ip= '10.0.0.1/8')
		q1 = [(r0, 'r0', '10.0.0.1/8')]
		q2 = []

		ipNums = [('r1', '10.0.0.1/16'), ('r2', '10.1.0.1/16'), ('r3', '10.0.1.1/24'),('r4', '10.0.2.1/24'), ('r5', '10.1.1.1/24'), ('r6', '10.1.2.1/24'),('r7', '10.0.1.224/28'), ('r8', '10.0.1.240/28'), ('r9', '10.0.2.224/28'), ('r10', '10.0.2.240/28'),('r11', '10.1.1.224/28'), ('r12', '10.1.1.240/28'), ('r13', '10.1.2.224/28'), ('r14', '10.1.2.2540/28')]

		for layer in range(1,4):
		    for r in range(2**layer):
			pRouter = q1.pop(0)

			#left child
			newData = ipNums.pop(0)
			newRouter = self.addNode(newData[0], cls=LinuxRouter, ip=newData[1])
			self.addLink(pRouter[0], newRouter, infName2=str(pRouter[1])+"-eth1", params2={'ip':newData[1]})
			q2.append((newRouter, newData[0], newData[1]))

			#right child
			newData = ipNums.pop(0)
			newRouter = self.addNode(newData[0], cls=LinuxRouter, ip=newData[1])
			self.addLink(pRouter[0], newRouter, infName2=str(pRouter[1])+"-eth2", params2={'ip':newData[1]})
			q2.append((newRouter, newData[0], newData[1]))
		    q1 = q2
		    q2 = []

		hostCounter = 0
		for router in q1:
		    startVal = router[2][7:-3]
		    ipRange = range(startVal+1, startVal+6)
		    for i in range(0, 5):
			host = self.addHost('h'+str(hostCounter),
			    'ip'+str(router[2][:7])+ipRange[i]+router[2][-3:],
			    defaultRouter='via ' + str(router[2][:-3]))
			self.addLink(host, router[0])

def run():
    "Test linux router"
    topo = MyTopo()
    net = Mininet( topo=topo )
    net.start()
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
