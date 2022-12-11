#!/usr/bin/python
import sys
import ipaddress
import socket
import json
from tabulate import tabulate
sys.path.insert(0,'./src') #Essential to import ece.py in uxdp.py
from src import ece
import os

def getHelp():
    help = """
    Usage: uxdp COMMAND

    Commands:
    enable                enables the firewall
    disable               disables the firewall
    allow ARGS            add allow rule
    deny ARGS             add deny rule
    limit ARGS            add limit rule
    delete RULE|NUM       delete RULE
    reload                reload firewall
    reset                 reset firewall
    status                show firewall status
    status numbered       show firewall status as numbered list of RULES
    version               display version information
    """
    print(help)
    return 1

def getFirewallconfig():
    """
    Read the firewall.json config rile
    :return: Json firewall
    """
    firewall = open('conf/firewall.json')
    return json.load(firewall)

def getFirewallstatus():
    """
    Return the firewall status
    :return: bool True|False (if firewall is active or not)
    """
    if (getFirewallconfig()['firewall_status']['status'] == "active" ):
        return True
    return False

def getAction():
    """
    Check if the action is present in the first argument
    (allow, deny, limit, version)

    :return: string of the action OR False If Not Found!
    """
    if ((len(sys.argv)-1) > 0):
        if (sys.argv[1] in ["allow", "deny", "limit", "version", "status", "enable", "disable", "delete", "reload"]):
            return sys.argv[1]
    return False

def deleteRule():
    if len(sys.argv) != 3:
        print("Can't delete this rule, see help")
        return 0
    ruleid = sys.argv[2]
    config = getFirewallconfig()
    if ruleid not in config['firewall']:
        print("Rule ID {} not found, see <uxdp status numbered> to get the rule id".format(ruleid))
        return 0
    del config['firewall'][ruleid]

    with open("conf/firewall.json", "w") as outfile:
        outfile.write(json.dumps(config, indent=4))
    print("Rule {} was successfully removed, don't forget to reload the firewall !".format(ruleid))
    return 1

def getVersion():
    print("UXDP (Uncomplicated eXpress Data Path) UXDP v1\nThis tool is provided for free under GNU License.\n\nFor help : uxdp help")
    return 1

def validateIp(iprange):
    """
    Get from an ip address associated
    :return: 1.1.1.1/24 or False
    """
    try:
        ipaddress.ip_network(iprange, strict=False)
        return iprange
    except:
        print("Unvalid ip address / range")
        return False

def getFirewallstatusNumbered():
    """
    Print all the firewall rule if argv find numbred at 3 and return state
    :return: bool
    """
    if ((len(sys.argv)-1) >= 2):
        if (sys.argv[2] == "numbered"):
            rules = getFirewallconfig()['firewall']
            head = ["Rule ID", "Interface", "Action",
            "Destination IP", "Source IP", "Protocol",
            "Source port", "Destination port", "Rate limit",
            "Comments"]
            data = []
            for rule in rules:
                r = rules[rule]
                data.append([
                rule, r["interface"], r["action"],
                r["ipdst"], r["ipsrc"], r["proto"],
                r["portdst"], r["portsrc"], r["limit"],
                r["comments"]])
            print(tabulate(data, headers=head, tablefmt="grid"))
            return True
    return False

def addRule(fwaction):
    """
    :param: fwaction str of the fw action (ACCEPT, DENY, LIMIT)
    Add a rule in the firewall.json config file
    """
    ipsrc, ipdst, portsrc, portdst, proto, limit, interface, comment = "", 0, 0, 0, "", 0, "", ""
    for arg in sys.argv:
        if "ipsrc" in arg:
            ip = arg.split("=")[1]
            if ip == "any" or validateIp(ip) != False:
                ipsrc = ip
        if "ipdst" in arg:
            ip = arg.split("=")[1]
            if ip == "any" or validateIp(ip) != False:
                ipdst = ip
        if "portsrc" in arg:
            portsrc = arg.split("=")[1]
        if "portdst" in arg:
            portdst = arg.split("=")[1]
        if "proto" in arg:
            p = arg.split("=")[1]
            if p in ["TCP", "UDP", "ICMP"]:
                proto = p
        if "limit" in arg:
            limit = arg.split("=")[1]
        if "interface" in arg:
            interface = arg.split("=")[1]
        if "comment" in arg:
            comment = arg.split("=")[1]
        
    if ipsrc == "" or proto == "" or interface == "":
        print("Please specify at least the interface, the ip source and the protocol")
        return 0
    
    # get the firewall config for the previous ID
    config = getFirewallconfig()
    if (len(config['firewall']) == 0):
        newid = 0
    else:
        lastid = int(max(config['firewall'].keys()))
        newid = str(lastid + 1)
    newrule = {
        "action": fwaction,
        "ipdst": ipdst,
        "ipsrc": ipsrc,
        "proto": proto,
        "portdst": portdst,
        "portsrc": portsrc,
        "limit": limit,
        "comments": comment,
        "interface": interface
    }
    config['firewall'][newid] = newrule
    with open("conf/firewall.json", "w") as outfile:
        outfile.write(json.dumps(config, indent=4))
    print("Rule {} was successfully added, don't forget to reload the firewall !".format(newid))
    return 1
    
def is_root():
    return os.geteuid() == 0

def main():
    if (not is_root()):
        print('This program required sudo.')
        sys.exit(1)
    action = getAction()
    if action == False:
        getHelp()
    if action == "version":
        getVersion()
    if action == "status":
        if getFirewallstatus():
            if getFirewallstatusNumbered():
                return 1
            else:
                print("UXDP status : active")
        else:
            print("UXDP status : inactive")
    if action == "delete":
        deleteRule()
    if action == "allow":
        addRule("ACCEPT")
    if action == "deny":
        addRule("DENY")
    if action == "limit":
        addRule("LIMIT")
    if action == "enable":
        #print("@TODO : enable the firewall...")
        ece.main(action)
    if action == "disable":
        #print("@TODO : disable the firewall...")
        ece.main(action)
    if action == "reload":
        #print("@TODO : reload the firewall...")
        ece.main(action)
    if action == "reset":
        #print("@TODO : reset the firewall...")
        ece.main(action)
    

if __name__ == '__main__':
    main()
