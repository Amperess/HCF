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
	    # Need to subtract one because diff between ttl and traceroute
            self.ipAddrsDict[ipAddr] = str(int(count)-1)

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

	if str(self.ipAddrsDict[ip]) != hc:
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
        print("Running traceroutes...")
	self.parseTraceRoutes(self.issueTraceRoutes(ipAddrs), ipAddrs)
	self.ipAddrsDict["10.0.2.101"] = "3"
	#self.ipAddrsDict["10.0.3.100"] = "3"
	print(self.ipAddrsDict)
