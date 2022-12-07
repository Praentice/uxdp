#!/usr/bin/python
import sys
import ipaddress
import socket
import json

def getAction():
    """
    Check if the action is present in the first argument
    (allow, deny, limit, version)

    :return: string of the action OR False If Not Found!
    """
    if ((len(sys.argv)-1) > 0):
        if (sys.argv[1] in ["allow", "deny", "limit", "version", "status"]):
            return sys.argv[1]
    return False

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
    status verbose        show verbose firewall status
    version               display version information
    """
    print(help)
    return 1

def getFromAndIp():
    """
    Get from and ip adress associeted
    from 1.1.1.1/24
    :return: ip range 1.1.1.1/24
    """
    if ((len(sys.argv)-1) > 2):
        if (sys.argv[2] == "from"):
            try:
                ipaddress.ip_network(sys.argv[3], strict=False)
                return sys.argv[3]
            except:
                return False
    return False

def getPortAndOrProto(frist=True):
    if ((len(sys.argv)-1) >= 2):
        ports = range(1, 65535)

        if ((sys.argv[2]).isnumeric()):
            if (int(sys.argv[2]) in ports):
                return sys.argv[2]
        
        split = sys.argv[2].split("/")
        if (len(split) > 1):
            if split[1] in ["tcp", "udp"]:
                return split
    return False

def getFirewallconfig():
    """
    Read the firewall.json config rile
    :return: Json firewall
    """
    firewall = open('./conf/firewall.json')
    return json.load(firewall)

def getFirewallstatus():
    """
    Return the firewall status
    :return: bool True|False (if firewall is active or not)
    """
    if (getFirewallconfig()['firewall_status']['status'] == "active" ):
        return True
    return False

def getFirewallstatusNumbered():
    """
    Print all the firewall rule if argv find numbred at 3 and return state
    :return: bool
    """
    if ((len(sys.argv)-1) >= 2):
        if (sys.argv[2] == "numbered"):
            rules = getFirewallconfig()['firewall']
            for rule in rules:
                print (rule)
            return True
    return False

def getVersion():
    print("UXDP (Uncomplicated eXpress Data Path) UXDP v1\nThis tool is provided for free under GNU License.\n\nFor help : uxdp help")
    return 1

def main():
    action = getAction()
    if action == False:
        getHelp()
    if action == "version":
        getVersion()
    if action == "status":
        if getFirewallstatus():
            if getFirewallstatusNumbered():
                print ("coucou")
            else:
                print("UXDP status : active")
        else:
            print("UXDP status : inactive")
    

    if action in ["allow", "deny", "limit"]:
        # parse others arguments
        print(getFromAndIp())
        print(getPortAndOrProto())


if __name__ == '__main__':
    main()
    