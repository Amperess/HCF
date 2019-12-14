# Hop Count Filtering
Implementing Hop Count Filtering method for DDoS prevention on a virtual network.

The goal of our project is to detect if a sender changed the source IP address on a packet header from their own address to another. A user may want to spoof their address to abuse fair bandwidth allocation algorithms by spraying packets under a variety of source addresses. This technique may also be used to send a flood of requests from different addresses to a single server to overload its resources and make it unavailable to its intended users in a Distributed Denial of Service (DDoS) attack.

Given the amount of reasons for why a user would want to spoof their IP address, detecting spoofed packets is an open research problem. The primary goal of our project is implementing the Hop Count Filtering method in a virtual network to test its effectiveness in detecting spoofed packets. The method uses the TTL field to correctly identify whether or not a host is transmitting/receiving packets with their true address.


# Installation
## Download Mininet

Follow the instructions at the following link to install the Mininet VM.

http://mininet.org/download/

Once downloaded, start up the VM. Login to it using the username: mininet and password: mininet.
It is helpful to install a GUI environment on the VM. Follow the instructions at:

https://github.com/mininet/mininet/wiki/FAQ#vm-console-gui

Once downloaded, the GUI can be started by typing: startx in the mininet command line.

## Dependencies
You may need to install dependencies to run the project like traceroute or git if they are not already on the machine. They can be installed using the following command:
```
$ sudo apt-get install traceroute
$ sudo apt install git
```
## Clone Repositories
With the GUI loaded, open a terminal window. Enter the following commands.

```
$ cd mininet
$ mkdir github
$ cd github
```
In this directory, we want to clone 2 repositories.

1. Clone this repository.

2. Follow the instructions to clone and set up Scapy (command line tool used for constructing and sending modified packets):

https://scapy.readthedocs.io/en/latest/installation.html


# Running Our Code

Run our topology: testrouter3.py with the following command in the VM:
```
$ sudo python testrouter3.py
```
In the mininet command line, open terminals for h1 and h2 using the following commands:
```
$ h1 xterm &
$ h2 xterm &
```
In h1's terminal, run the following command:
```
# python filterServer.py
```
The program may take some time to run the trace routes needed to form the table. Wait until a dictionary of IP addresses to hop counts is printed.
Meanwhile, in h2's terminal, change to the Scapy directory. The setup step should already be completed. Start Scapy with the command:
```
# sudo ./run_scapy
```

## Sending a Normal Packet
Craft the packet in Scapy on h2 by typing:
```
$ packet=IP(ttl=60,src="10.0.2.100",dst="10.0.1.100")/UDP()
```
Once the server has printed the dictionary in h1's terminal, send the packet from h2 using the command:
```
$ send(packet)
```
You can examine h1's terminal to see the effects of recieving the packet.

## Sending a Spoofed Packet
Craft the packet in Scapy by typing:
```
$ packet=IP(ttl=60,src="10.0.2.101",dst="10.0.1.100")/UDP()
```
Once again, send the packet using:
```
$ send(packet)
```
This time, h1 should have registered it as spoofed.
