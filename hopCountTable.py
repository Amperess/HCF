import os

class HopCountTable():

    ipAddrsDict = {}

    '''
    Given traceroute responses, populate the ipAddrsDict with
    indices as the indices and hop counts as the values
    '''
    def parseTraceRoutes(self, resps, ipAddrs):
        for resp, ipAddr in zip(resps, ipAddrs):
            linesList = resp.split("\n")
            lastLine = linesList[len(linesList)-1]
            if len(lastLine) < 2:
                lastLine = linesList[len(linesList)-2]
            count = lastLine.split(" ")[0]
            try:
                int(count)
            except:
                count = lastLine.split(" ")[1]
            self.ipAddrsDict[ipAddr] = count

    '''
    Given a list of IP addresses, run traceroutes on each of them and
    record the responses
    '''
    def issueTraceRoutes(self, ipAddrs):
        resps = []
        for ipAddr in ipAddrs:
            resps.append(os.popen("traceroute " + ipAddr).read())
        return resps


    '''
    Given an IP address and a hop count calculated from the TTL
    return True if it doesn't match (and therefore is spoofed)
    and False otherwise
    '''
    def hcLookup(self, ip, hc):
        hc = str(hc)
        if self.ipAddrsDict[ip] != hc:
            return True
        else:
            return False

    '''
    Given an IP address and a hop count calculated from the TTL
    return True if it doesn't fall between the expected hc - diff and
    expected hc + diff (and therefore is spoofed) and False otherwise
    '''
    def hcLookupRange(self, ip, hc, diff):
        hc = int(hc)
        diff = int(diff)
        expected_hc = int(self.ipAddrsDict[ip])
        if hc > (expected_hc + diff) or hc < (expected_hc - diff):
            return True
        else:
            return False

    '''
    If an address seemed spoofed but it formed a legit TCP connection
    update the entry with the updated hop count
    '''
    def updateEntry(self, ip, hc):
        self.ipAddrsDict[ip] = str(hc)

    '''
    Initialize a table with the given ip addresses
    '''
    def __init__(self, ipAddrs):
        self.parseTraceRoutes(self.issueTraceRoutes(ipAddrs), ipAddrs)

'''
class run():
    if __name__ == '__main__':
        ipAddrs = ["172.217.12.206", "31.13.71.36", "128.6.43.6"]
        hcp = HopCountTable(ipAddrs)
        print("Hello world")
        print(hcp.ipAddrsDict)
        print(hcp.hcLookup("128.6.43.6", 6))
        print(hcp.hcLookupRange("128.6.43.6", 6, 2))
        hcp.updateEntry("128.6.43.6", 6)
        print(hcp.ipAddrsDict)
'''
