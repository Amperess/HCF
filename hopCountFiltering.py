from hopCountTable import HopCountTable

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

    """
    Change state from 0 (alert, no dropping) and 1 (action, drop spoofed packets)
    """
    def switch_state(self):
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0

    """
    Given a packet, lookup it's initial TTL from it's actual TTL and check if
    it's spoofed
    """
    def inspect_packet(self, packet):
        ttl = packet['ttl']
        src = packet['src']

        # choose the smallest initial TTL that is larger than it
        initialTTL = 2
        for i in self.initialTTLs:
            if ttl < i:
                initialTTL = i
                break
        hc = initialTTL - ttl

        # We can only update the table if a legit TCP connection is formed
        # by a "spoofed" user, showing a legit different hop count

        # if not self.hct.hcLookup(src, hc):
        #    self.hct.updateEntry(src, hc)

        return self.hct.hcLookup(src, hc)

    """
    Check the last 30 packets to see the average number of spoofed packets
    """
    def average(self, spoofed):
        self.l.append(spoofed)
        self.l.pop(0)
        return sum(self.l)/len(self.l)

    """
    Return 1 to accept or -1 to flag as spoofed and -2 to drop
    """
    def accept_packet(self, packet):
        while True:
            spoofed = self.inspect_packet(packet)
            t = self.average(spoofed)
            if self.state:
                if t <= self.threshold_action:
                    self.switch_state()
                if spoofed:
                    self.dropped += 1
                    return -2
                else:
                    self.accepted += 1
                    return 1
            else:
                if spoofed:
                    if t > self.threshold_alert:
                        self.switch_state()
                self.accepted += 1
                return -1
