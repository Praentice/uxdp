#!/usr/bin/env python3
#from bcc import BPF
import os
import subprocess
import json
import sys
import shutil


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
        sourceCode = generateSourceCodePerNetworkInterface(networkInterface,rules) #We generate the firewall source code 
        #writeSourceCode(sourceCode) # We write the generated firewall source code to the file
        #fileNameCompiledCode = compileSourceCode(fileName) # We compile the firewall source code
        #executeCompiledProgram(fileNameCompiledCode) # We apply the firewall program on the network interface


def generateSourceCodePerNetworkInterface(networkInterface,rules): #Generate the firewall source code based on the configuration retrieved from the file ./conf/firewall.json
    #\t = tabulation char for indentation
    #\n = new line char for new line 
    firewallFile = open("./firewall/source/"+"uxdp_"+networkInterface+"_firewall.c",'r')
    for line in firewallFile:
        print(line)
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
        p = subprocess.Popen('sudo ip link set '+networkInterface+' xdpgeneric obj '+fileNameToCall+'sec firewall', shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    except Exception as e:
        print("The error raised during the execution is : {}".format(e))

if __name__ == '__main__':
    configuration = getCurrentConfigurationFile() # We retrieve the configuration file content
    networkInterfacesList = getAllNetworkInterfaces(configuration["firewall"]) # We retrieve the network interfaces based on the configuration file
    rulesPerNetworkInterfaces = sortingAllRulesToTheNetworkInterfaces(configuration,networkInterfacesList) # We sort the rules based on the network interface they apply
    createFilesPerNetworkInterface(networkInterfacesList) # We create a firewall from a template for each network interface
    applyRules(rulesPerNetworkInterfaces) # We apply the rules configured by the user
    
