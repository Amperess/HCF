import os

ipAddrs = ["172.217.12.206", "31.13.71.36", "128.6.43.6"]
ipAddrsDict = {}

class hopCountTable():

    '''
    Given traceroute responses, populate the ipAddrsDict with
    indices as the indices and hop counts as the values
    '''
    def parseTraceRoutes(resps, ipAddrs):
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
            ipAddrsDict[ipAddr] = count

    '''
    Given a list of IP addresses, run traceroutes on each of them and
    record the responses
    '''
    def issueTraceRoutes(ipAddrs):
        resps = []
        for ipAddr in ipAddrs:
            resps.append(os.popen("traceroute " + ipAddr).read())
        return resps


    '''
    Given an IP address and a hop count calculated from the TTL
    return True if it doesn't match (and therefore is spoofed)
    and False otherwise
    '''
    def hcLookup(ip, hc):
        hc = str(hc)
        if ipAddrsDict[ip] != hc:
            return True
        else:
            return False

    if __name__ == '__main__':
        parseTraceRoutes(issueTraceRoutes(ipAddrs), ipAddrs)
        print(ipAddrsDict)
        print(hcLookup("128.6.43.6", 5))
