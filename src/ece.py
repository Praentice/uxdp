#!/usr/bin/env python3
import os
import subprocess
import json
import sys
import shutil
import fileinput
import binascii
import socket
import struct

# Beginning of the section for C source code
GENERATED_CODE = "            if (MODULE_PORT_DEST && MODULE_PORT_SRC) { //COMMENT \n		          if (MODULE_IP_SRC && MODULE_IP_DEST) {\n			          return XDP_PASS;\n		          }\n            }\n//GENERATED_CODE_"

MODULE_PORT_DEST = "(PROTOCOL->dest == ntohs(PORT_DEST))"
MODULE_PORT_DEST_RANGE = "(PROTOCOL->dest >= ntohs(PORT_RANGE_MIN)) && (PROTOCOL->dest <= ntohs(PORT_RANGE_MAX))"

MODULE_PORT_SRC = "(PROTOCOL->source == ntohs(PORT_SRC))"
MODULE_PORT_SRC_RANGE = "(PROTOCOL->source >= ntohs(PORT_RANGE_MIN)) && (PROTOCOL->source <= ntohs(PORT_RANGE_MAX))"

MODULE_IP_SRC = "(ip->saddr == IP_ADDR_SRC)"
MODULE_IP_SRC_NETWORK = "(is_ip_address_in_network(ip->saddr,ntohl(NETIP),ntohl(NETMASK)))"

MODULE_IP_DEST = "(ip->daddr == IP_ADDR_DEST)"
MODULE_IP_DEST_NETWORK = "(is_ip_address_in_network(ip->daddr,ntohl(NETIP),ntohl(NETMASK)))"
# Ending of the section for C source code

def cidrToNetmask(cidr):
    network, net_bits = cidr.split('/')
    host_bits = 32 - int(net_bits)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return network, netmask

def getCurrentConfigurationFile(): #Retrieve the content of the configuration file in the conf folder
    fileObject = open("./conf/firewall.json", "r")
    jsonContent = fileObject.read()
    configuration = json.loads(jsonContent)
    return configuration

def getAllNetworkInterfaces(configuration):
    networkInterfacesList = []
    for k in range(len(configuration)):
        interface = configuration[str(k)]["interface"]
        if interface not in networkInterfacesList:
            networkInterfacesList.append(interface)
    return networkInterfacesList

def sortingAllRulesToTheNetworkInterfaces(configuration,interfaces):
        dictionnary = {}
        for i in interfaces:
            dictionnary[i]=[]
            for k in configuration["before_rules"]:
                dictionnary[i].append(configuration["before_rules"][k])
            for j in configuration["firewall"]:
                if i == configuration['firewall'][j]['interface']:
                    dictionnary[i].append(configuration['firewall'][j])
        return dictionnary

def createFilesPerNetworkInterface(networkInterfacesList):
    for i in networkInterfacesList:
        shutil.copyfile('./firewall/template/uxdp_template_firewall.c','./firewall/source/uxdp_'+i+'_firewall.c')

def applyRules(rulesPerNetworkInterfaces):
    for networkInterface in rulesPerNetworkInterfaces: #For each network interfaces
        rules = rulesPerNetworkInterfaces[networkInterface] #We retrieve the rules
        generateSourceCodePerNetworkInterface(networkInterface,rules) #We generate the firewall source code 
        errorCode = compileSourceCode(networkInterface) # We compile the firewall source code
        if errorCode == 1:
            print("Error during the compilation of the firwall for this network interface : {}".format(networkInterface))
        else :
            executeCompiledProgram(networkInterface) # We apply the firewall program on the network interface


def generateSourceCodePerNetworkInterface(networkInterface,rules): #Generate the firewall source code based on the configuration retrieved from the file ./conf/firewall.json
    #\t = tabulation char for indentation
    #\n = new line char for new line 
    for rule in rules:
        generateAndWriteOneRule(networkInterface,rule)

def generateAndWriteOneRule(networkInterface,rule):
#\t = tabulation char for indentation
    #\n = new line char for new line 
    fileName = "./firewall/source/"+"uxdp_"+networkInterface+"_firewall.c"
    newLine = ""
    firewallFile = open(fileName,'r')
    ruleWrittenInC = GENERATED_CODE
    ruleWrittenInC = ruleWrittenInC.replace("PROTOCOL",rule['proto']) #Fill the generated code with the appropriate protocol
    ruleWrittenInC = ruleWrittenInC.replace("COMMENT"," "+rule['comments']) #Fill the generated code with the comments
    if (type(rule['portdst']) is str): # Generate code to check the destination port
        if ("," in rule["portdst"]):
            ports = rule['portdst'].split(",")
            k = 0
            finalCondition = ""
            for i in range(len(ports)+1):
                print(i)
                if (i%2 == 0):
                    conditionPortDst = MODULE_PORT_DEST
                    conditionPortDst = conditionPortDst.replace("PROTOCOL",rule['proto'].lower())
                    conditionPortDst = conditionPortDst.replace("PORT_DEST",ports[k])
                    finalCondition = finalCondition+conditionPortDst
                    k = k+1
                else:
                    finalCondition = finalCondition+" || "
            ruleWrittenInC = ruleWrittenInC.replace("MODULE_PORT_DEST","("+finalCondition+")")

        elif ("-" in rule["portdst"]):
            port_min = rule['portdst'].split("-")[0]
            port_max = rule['portdst'].split("-")[1]
            module_port_dest = MODULE_PORT_DEST_RANGE
            module_port_dest = module_port_dest.replace("PORT_RANGE_MIN",port_min)
            module_port_dest = module_port_dest.replace("PORT_RANGE_MAX",port_max)
            ruleWrittenInC = ruleWrittenInC.replace("MODULE_PORT_DEST",module_port_dest)
        else :
            module_port_dest = MODULE_PORT_DEST
            module_port_dest = module_port_dest.replace("PORT_DEST",rule['portdst'])
            ruleWrittenInC = ruleWrittenInC.replace("MODULE_PORT_DEST",module_port_dest)
    else : # No specified destination port
            ruleWrittenInC = ruleWrittenInC.replace("MODULE_PORT_DEST","(0 < 1)")

    if (type(rule['portsrc']) is str): # Generate code to check the source port
        if ("," in rule["portsrc"]):
            ports = rule['portsrc'].split(",")
            k = 0
            finalCondition = ""
            for i in range(len(ports)):
                if (i%2 == 0):
                    conditionPortSrc = MODULE_PORT_SRC
                    conditionPortSrc =conditionPortSrc.replace("PROTOCOL",rule['proto'].lower())
                    conditionPortSrc =conditionPortSrc.replace("PORT_SRC",ports[k])
                    finalCondition = finalCondition+conditionPortSrc
                    k = k+1
                else:
                    finalCondition = finalCondition+" || "
            ruleWrittenInC = ruleWrittenInC.replace("MODULE_PORT_SRC","("+finalCondition+")")
            
        elif ("-" in rule["portsrc"]):
            port_min = rule['portsrc'].split("-")[0]
            port_max = rule['portsrc'].split("-")[1]
            module_port_src = MODULE_PORT_SRC_RANGE
            module_port_src = module_port_src.replace("PORT_RANGE_MIN",port_min)
            module_port_src = module_port_src.replace("PORT_RANGE_MAX",port_max)
            ruleWrittenInC = ruleWrittenInC.replace("MODULE_PORT_SRC",module_port_src)
        else :
            module_port_src = MODULE_PORT_SRC
            module_port_src = module_port_src.replace("PORT_SRC",rule['portsrc'])
            ruleWrittenInC = ruleWrittenInC.replace("MODULE_PORT_SRC",module_port_src)
    else:
        ruleWrittenInC = ruleWrittenInC.replace("MODULE_PORT_SRC","(0 < 1)")

    if (type(rule['ipsrc']) is str): # Generate code to check the source port
        if ("/" in rule["ipsrc"]):
            conditionIpSrc = MODULE_IP_SRC_NETWORK
            networkAddrInStr,networkMaskInStr = cidrToNetmask(rule["ipsrc"])
            networkAddrInHex = "0x"+((binascii.hexlify(socket.inet_aton(networkAddrInStr)).decode('utf-8'))).upper()
            networkMaskInHex = "0x"+((binascii.hexlify(socket.inet_aton(networkMaskInStr)).decode('utf-8'))).upper()
            conditionIpSrc  = conditionIpSrc .replace("NETIP",networkAddrInHex)
            conditionIpSrc  = conditionIpSrc .replace("NETMASK",networkMaskInHex)
            k = 0
            ruleWrittenInC = ruleWrittenInC.replace("MODULE_IP_SRC","("+conditionIpSrc +")")
        else :
            module_ip_src = MODULE_IP_SRC
            module_ip_src = module_ip_src.replace("IP_ADDR_SRC","\""+rule['ipsrc']+"\"")
            ruleWrittenInC = ruleWrittenInC.replace("MODULE_IP_SRC",module_ip_src)
    else:
        ruleWrittenInC = ruleWrittenInC.replace("MODULE_IP_SRC","(1 > 0)")
    
    if (type(rule['ipdst']) is str): # Generate code to check the source port
        if ("/" in rule["ipdst"]):
            conditionIpDest = MODULE_IP_DEST_NETWORK
            networkAddrInStr,networkMaskInStr = cidrToNetmask(rule["ipdst"])
            networkAddrInHex = "0x"+((binascii.hexlify(socket.inet_aton(networkAddrInStr)).decode('utf-8'))).upper()
            networkMaskInHex = "0x"+((binascii.hexlify(socket.inet_aton(networkMaskInStr)).decode('utf-8'))).upper()
            conditionIpDest = conditionIpDest.replace("NETIP",networkAddrInHex)
            conditionIpDest = conditionIpDest.replace("NETMASK",networkMaskInHex)
            k = 0
            ruleWrittenInC = ruleWrittenInC.replace("MODULE_IP_DEST","("+conditionIpDest+")")
        else :
            module_ip_dest = MODULE_IP_DEST
            module_ip_dest = module_ip_dest.replace("IP_ADDR_DEST","\""+rule['ipdst']+"\"")
            ruleWrittenInC = ruleWrittenInC.replace("MODULE_IP_DEST",module_ip_dest)
    else:
        ruleWrittenInC = ruleWrittenInC.replace("MODULE_IP_DEST","(1 > 0)")

    ruleWrittenInC = ruleWrittenInC.replace("//GENERATED_CODE_","//GENERATED_CODE_"+rule['proto'])
    ruleWrittenInC = ruleWrittenInC.replace("PROTOCOL",rule['proto'].lower())
    firewallFile.close()
    for line in fileinput.input(fileName, inplace=1):
        if '//GENERATED_CODE_'+rule['proto'] in line:
            line = line.replace('//GENERATED_CODE_'+rule['proto'],ruleWrittenInC)
        sys.stdout.write(line)
    resultat = 0
    return resultat

def writeSourceCode(sourceCode): #Write the generated firewall source code into a file
    sourceCodeFileName = "./firewall/firewall.c" 
    try:
        with open(sourceCodeFileName, 'w') as FOUT: #Write source code to the file named with the value of the variable fileName
            FOUT.write(sourceCode)
        FOUT.close() #Save the source code file
        return 0
    except Exception as e:
        return e #In case something went wrong

def compileSourceCode(networkInterface): #Compiled the firewall source code file to get a binary
    try:
        #clang -O2 -g -Wall -target bpf -c {} -o {}.format("./firewall/source/"+"uxdp_"+networkInterface+"_firewall.c","./firewall/exec/"+"uxdp_"+networkInterface+"_firewall.o")
        clangCommand = "clang -O2 -g -Wall -target bpf -c {} -o {}".format("./firewall/source/"+"uxdp_"+networkInterface+"_firewall.c","./firewall/exec/"+"uxdp_"+networkInterface+"_firewall.o")
        subprocess.call(clangCommand, shell=True)
        return 0
    except Exception as e:
        print("The error raised during the compilation is : {}".format(e))
        return 1

def executeCompiledProgram(networkInterface): #Execute the firewall program and push it to the right network interface
    fileNameToCall = "./firewall/exec/"+"uxdp_"+networkInterface+"_firewall.o"
    #To unload the firewall : sudo ip link set veth1 xdpgeneric obj xdp_drop.o sec xdp_drop
    try:
        p = subprocess.Popen('ip link set '+networkInterface+' xdpgeneric obj '+fileNameToCall+' sec firewall', shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    except Exception as e:
        print("The error raised during the execution is : {}".format(e))

def unloadFirewall(networkInterface):
    try:
        #sudo ip link set veth1 xdpgeneric off
        p = subprocess.Popen('ip link set '+networkInterface+' xdpgeneric off', shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    except Exception as e:
        print("The error raised during the execution is : {}".format(e))


def main(action, interfaces=0):
    if (action == "enable"): # User wants to enable the firewall
        configuration = getCurrentConfigurationFile() # We retrieve the configuration file content
        networkInterfacesList = getAllNetworkInterfaces(configuration["firewall"]) # We retrieve the network interfaces based on the configuration file
        rulesPerNetworkInterfaces = sortingAllRulesToTheNetworkInterfaces(configuration,networkInterfacesList) # We sort the rules based on the network interface they apply
        createFilesPerNetworkInterface(networkInterfacesList) # We create a firewall from a template for each network interface
        applyRules(rulesPerNetworkInterfaces) # We apply the rules configured by the user
    if (action == "disable"): # User wants to disable the firewall
        if (interfaces == 0): # Apply disable action to all network interface
            configuration = getCurrentConfigurationFile() # We retrieve the configuration file content
            networkInterfacesList = getAllNetworkInterfaces(configuration["firewall"])
            for i in networkInterfacesList:
                unloadFirewall(i)
        else:
            for interface in (interfaces): # Apply disable action to specifics network interfaces
                unloadFirewall(interface)
    if (action == "reload"): # User wants to reload the firewall
        if (interfaces == 0): # Apply reload aéction to all network interface
            configuration = getCurrentConfigurationFile() # We retrieve the configuration file content
            networkInterfacesList = getAllNetworkInterfaces(configuration["firewall"])
            for i in networkInterfacesList:
                unloadFirewall(i)
                executeCompiledProgram(i)
        else:
            for interface in (interfaces): #Apply reload action to specifics network interfaces
                unloadFirewall(interface)
                executeCompiledProgram(interface)
if __name__ == '__main__':
    print("ERROR : You must call the ece.py script by using uxdp.py script !")
    
    
    
    
