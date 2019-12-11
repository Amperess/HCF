#!/usr/bin/python

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

    router1 = net.get('router1')
    router2 = net.get('router2')

    router1.cmd('ip route add 10.0.2.0/24 dev r1-eth0')    
    router2.cmd('ip route add 10.0.1.0/24 dev r2-eth0')

    info( '*** Routing Table on Router:\n' )
    info( net[ 'router1' ].cmd( 'route' ) )
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
