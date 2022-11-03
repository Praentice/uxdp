import os
import subprocess
import json
import sys

def generateSourceCode(configuration): #Generate the firewall source code based on the configuration retrieved from the file ./conf/firewall.json
    sourceCode = r'''
    #include <stdio.h>
    int main() {
        for(int i=0;i<5;i++) {
            printf("Testing %d\n",i);
        }
        return 0;
    }
    '''
    sourceCodeInOneLine = '#include <stdio.h>\nint main() {\n\tfor(int i=0;i<5;i++) {\n\t\tprintf("Testing %d\\n",i);\n\t}\n\treturn 0;\n}'
    return sourceCodeInOneLine

def writeSourceCode(sourceCode): #Write the generated firewall source code into a file
    sourceCodeFileName = "./firewall/firewall.c" 
    try:
        with open(sourceCodeFileName, 'w') as FOUT: #Write source code to the file named with the value of the variable fileName
            FOUT.write(sourceCode)
        FOUT.close() #Save the source code file
        return 0
    except Exception as e:
        return e #In case something went wrong
    

def compileSourceCode(): #Compiled the firewall source code file to get a binary
    try:
        gccCommand = "gcc {} -o {}".format('./firewall/firewall.c', './firewall/firewall')
        subprocess.call(gccCommand, shell=True)
        return 0
    except Exception as e:
        print("The error raised during the compilation is : {}".format(e))
        return 1

def executeAndReadCompiledProgram(): #Execute the firewall program and push it to the right network interface
    try:
        p = subprocess.Popen('./firewall/firewall', shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        for line in p.stdout:
            print(line) #To print or not to print, that is the question
    except Exception as e:
        print("The error raised during the execution is : {}".format(e))

def getCurrentConfigurationFile(): #Retrieve the content of the configuration file in the conf folder
    fileObject = open("./conf/firewall.json", "r")
    jsonContent = fileObject.read()
    configuration = json.loads(jsonContent)
    return configuration

def getAllNetworkInterfaces(configuration):
    print(configuration['0'])
    networkInterfacesList = []
    for k in range(len(configuration)):
        interface = configuration[str(k)]["interface"]
        if interface not in networkInterfacesList:
            networkInterfacesList.append(interface)
    return networkInterfacesList
        


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
    #rulesPerNetworkInterfaces = sortingAllRulesToTheNetworkInterfaces() # Rewrite the configuration rules to associate each rules to the corresponding interfaces
    #for firewallConfig in rulesPerNetworkInterfaces: #Write firewall rules in a specific source code for each network interfaces
    sourceCode = generateSourceCode(configuration) #Generate the source code for an interface
    returnValue = writeSourceCode(sourceCode) #Write the generated source code to a file
    executeAndReadCompiledProgram()
    
