#!/usr/bin/python3
import subprocess
import sys
import os
import json
VERSION=0.01

def exampleFunction(test1,test2): #Template function
    return test1,test2

def generateConfigurationFile(): #Generate the configuration file called firewall.json in the conf folder
    configuration = {"before_rules": {
        "0": {
            "action": "ACCEPT",
            "proto": "ICMP",
            "comments": "Allow ICMP by default"
        },
        "1": {
            "action": "ACCEPT",
            "proto": "DHCP",
            "comments": "Allow DHCP by default"
        },
        "2": {
            "action": "ACCEPT",
            "proto": "MULTICAST",
            "comments": "Allow DHCP by default"
        }
    }}, #Template for the configuration of a network port
    jsonString = json.dumps(configuration, indent=4) #Convert dictionnary to json format
    jsonFile = open("./conf/firewall.json", "w") #Create a new file called firewall.json in the folder confg
    jsonFile.write(jsonString) #Write the generated configuration into the file
    jsonFile.close() #Close the file

def getCurrentConfigurationFile(): #Retrieve the content of the configuration file in the conf folder
    fileObject = open("./conf/firewall.json", "r")
    jsonContent = fileObject.read()
    configuration = json.loads(jsonContent)
    return configuration

def writeSourceCode(configuration):
    sourceCode = r'''
    #include <stdio.h>
    int main() {
        for(int i=0;i<5;i++) {
            printf("Testing %d\n",i);
        }
        return 0;
    }
    '''
    sourceCodeFileName = "./firewall/firewall.c" #Default name for the sourceCode
    with open(sourceCodeFileName, 'w') as FOUT: #Write source code to the file named with the value of the variable fileName
        FOUT.write(sourceCode)
    FOUT.close() #Save the source code file
    return sourceCodeFileName

def compileSourceCode():
    try:
        gccCommand = "gcc {} -o {}".format('./firewall/firewall.c', './firewall/firewall')
        subprocess.call(gccCommand, shell=True)
        return 0
    except Exception as e:
        print("The error raised during the compilation is : {}".format(e))
        return 1
def executeAndReadCompiledProgram():
    try:
        p = subprocess.Popen('./firewall/firewall', shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        for line in p.stdout:
            print(line) #To print or not to print, that is the question
    except Exception as e:
        print("The error raised during the execution is : {}".format(e))

if __name__ == '__main__':
    #Getting args from user
    configuration = {}
    #Check if user run this program for the first time
    if (os.path.exists('./conf/firewall.json') == False):
        generateConfigurationFile() #We generate the configuration file
    configuration = getCurrentConfigurationFile() #We retrieve the configuration from the json file
    print(configuration)
    print(sys.argv)
    # Once we have retrieved the configuration file, we can begin to treat the user command.
    if sys.argv[1] == "allow":
        print("allow")
    elif sys.argv[1] == "limit":
        print("allow")
    elif sys.argv[1] == "deny":
        print("allow")
    elif sys.argv[1] == "reset":
        print("allow")
    elif sys.argv[1] == "reload":
        print("allow")
    else:
        print("xxx")
    sourceCodeFileName = writeSourceCode(configuration)
    returnValue = compileSourceCode()
    if returnValue == 0:
        executeAndReadCompiledProgram()  # Run the compiled programm











