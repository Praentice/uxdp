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
    for networkInterface in rulesPerNetworkInterfaces:
        rules = rulesPerNetworkInterfaces[networkInterface]
        sourceCode = generateSourceCodePerNetworkInterface(networkInterface,rules)
        print(sourceCode)
        #writeSourceCode(sourceCode)
        #fileNameCompiledCode = compileSourceCode(fileName)
        #executeCompiledProgram(fileNameCompiledCode)


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
    '''
    try:
        configuration = getCurrentConfigurationFile()
        #print(configuration["firewall"]) #Print the configuration retrieved by the program for debugging purposes
        networkInterfacesList = getAllNetworkInterfaces(configuration["firewall"]) # Retrieve all differents network interfaces mentionned in the configuration file
        sourceCode = generateSourceCode(configuration)
        returnValue = writeSourceCode(sourceCode) 
        if returnValue == 0: #Check if the source code writing went well
            returnValue = compileSourceCode() 
            if returnValue == 0: #Check if the compilation went well
                executeAndReadCompiledProgram()  # Run the compiled programm
            else : #Only executed in case the compilation went wrong
                print("Inexcepted issue, exiting...")
                os._exit(2)
            os._exit(0)
        else: #Only executed in case the source code writing went wrong
            print("An error was raised during the generation of the firewall : {}".format(returnValue))
            os._exit(1)
    except Exception as e:
        print("The error raised is : {}".format(e))
    '''
    configuration = getCurrentConfigurationFile()
    #print(configuration["firewall"]) #Print the configuration retrieved by the program for debugging purposes
    networkInterfacesList = getAllNetworkInterfaces(configuration["firewall"]) # Retrieve all differents network interfaces mentionned in the configuration file
    #print(networkInterfacesList)
    rulesPerNetworkInterfaces = sortingAllRulesToTheNetworkInterfaces(configuration,networkInterfacesList) # Rewrite the configuration rules to associate each rules to the corresponding interfaces
    #print(rulesPerNetworkInterfaces)
    createFilesPerNetworkInterface(networkInterfacesList)
    applyRules(rulesPerNetworkInterfaces)
    
