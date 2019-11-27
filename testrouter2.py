#!/usr/bin/python

"""
linuxrouter.py: Example network with Linux IP router
This example converts a Node into a router using IP forwarding
already built into Linux.
The example topology creates a router and three IP subnets:
    - 192.168.1.0/24 (r0-eth1, IP: 192.168.1.1)
    - 172.16.0.0/12 (r0-eth2, IP: 172.16.0.1)
    - 10.0.0.0/8 (r0-eth3, IP: 10.0.0.1)
Each subnet consists of a single host connected to
a single switch:
    r0-eth1 - s1-eth1 - h1-eth0 (IP: 192.168.1.100)
    r0-eth2 - s2-eth1 - h2-eth0 (IP: 172.16.0.100)
    r0-eth3 - s3-eth1 - h3-eth0 (IP: 10.0.0.100)
The example relies on default routing entries that are
automatically created for each router interface, as well
as 'defaultRoute' parameters for the host interfaces.
Additional routes may be added to the router or hosts by
executing 'ip route' or 'route' commands on the router or hosts.
"""


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


class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    def build( self, **_opts ):

        router1 = self.addNode('router1', cls=LinuxRouter)
	router2 = self.addNode('router2', cls=LinuxRouter)

        self.addLink( router1, router2, intfName1='r1-eth0', intfName2='r2-eth0',params1={'ip': '10.0.3.10/24'}, params2={ 'ip' : '10.0.3.20/24' } )

	h1 = self.addHost( 'h1', ip='10.0.1.100/24',
                           defaultRoute='via 10.0.1.10' )
        h2 = self.addHost( 'h2', ip='10.0.2.100/24',
                           defaultRoute='via 10.0.2.100' )
	self.addLink( router1, h1, intfName1='r1-eth1', intfName2='h1-eth0', params1 = {'ip':'10.0.1.10/24'}, params2={'ip':'10.0.1.100/24'})
	self.addLink( router2, h2, intfName1='r2-eth1', intfName2='h2-eth0', params1 = {'ip':'10.0.2.20/24'}, params2={'ip':'10.0.2.100/24'})
def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo )  # controller is used by s1-s3
    net.start()
    info( '*** Routing Table on Router:\n' )
    info( net[ 'router1' ].cmd( 'route' ) )
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
