from hopCountTable import HopCountTable
from scapy.all import *

"""
Manages the state between alert and action
"""
class HCFStateManager():

    """
    0 if alert, 1 if action
    """

    def __init__(self, ipAddrs, threshold_alert, threshold_action):
        self.hct = HopCountTable(ipAddrs)
        self.ipAddrs = ipAddrs
        self.state = 0
        self.dropped = 0
        self.accepted = 0
        self.initialTTLs = [2, 10, 30, 32, 60, 64, 128, 255]
        self.threshold_alert = threshold_alert
        self.threshold_action = threshold_action
        self.l = []
        for i in range(30):
            self.l.append(0)

    def switch_state(self):
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0

    def inspect_packet(self, packet):
        ttl = packet.ttl
        src = packet.src
        initialTTL = 2
        for i in self.initialTTLs:
            if ttl < i:
                initialTTL = i
                break
        hc = initialTTL - ttl
        if not self.hct.hcLookup(src, hc):
            self.hct.updateEntry(src, hc)
        return self.hct.hcLookup(src, hc)

    def average(self, spoofed):
        self.l.append(spoofed)
        self.l.pop(0)
        return sum(self.l)/len(self.l)

    """
    Need to run scapy server on the nodes
    scapy.srloop(pingr)
    """
    def run(self):
        while True:
            unans, ans = sr(packet)
            spoofed = self.inspect_packet(ans)
            t = self.average(spoofed)
            if self.state:
                if spoofed:
                    self.dropped += 1
                else:
                    self.accepted += 1
                if t <= self.threshold_action:
                    self.switch_state()
            else:
                if spoofed:
                    if t > self.threshold_alert:
                        self.switch_state()
                self.accepted += 1
