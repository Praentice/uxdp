#!/usr/bin/python3
import argparse
import subprocess
import sys
import os
VERSION=0.01

def exampleFunction(test1,test2):
    return test1,test2

def printIfNeeded(stringToPrint,canIPrintThisMessage):
    if canIPrintThisMessage:
        print(stringToPrint)
def writeSourceCode(sourceCode):
    sourceCodeFileName = "./firewall.c" #Default name for the sourceCode
    with open(sourceCodeFileName, 'w') as FOUT: #Write source code to the file named with the value of the variable fileName
        FOUT.write(sourceCode)
    FOUT.close() #Save the source code file
    return sourceCodeFileName

def compileSourceCode(sourceCodeFileName,compiledFileName,canIPrintThisMessage):
    try:
        gccCommand = "gcc {} -o {}".format(sourceCodeFileName, compiledFileName)
        subprocess.call(gccCommand, shell=True)
        return 0
    except Exception as e:
        printIfNeeded("The error raised during the compilation is : {}".format(e),canIPrintThisMessage)
        return 1
def executeAndReadCompiledProgram(executeCommand,canIPrintThisMessage):
    try:
        p = subprocess.Popen(executeCommand, shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        for line in p.stdout:
            printIfNeeded(line,canIPrintThisMessage) #To print or not to print, that is the question
    except Exception as e:
        printIfNeeded("The error raised during the execution is : {}".format(e), canIPrintThisMessage)


def getOptions():
    parser = argparse.ArgumentParser(add_help=True, formatter_class=argparse.RawTextHelpFormatter,description=
    """
    XUFW                  
    This CLI tool allows you to easily configure a firewall using the XDP technology on your server
    """,
    epilog=
    """
    This tool is provided for free under GNU/GPLv3 License.
    """,
    )
    parser.version = "The current version is {}".format(VERSION)
    # Section for mandatory arguments and flag
    #parser.add_argument('-n1', "--nothing1", required=True,help="""Nothing here. (Mandatory)""",nargs='+')
    # Section for optional arguments and flag
    parser.add_argument('-n2', "--nothing2", required=False,action='store_true', help="""Nothing here. (Optionnal)""", )
    parser.add_argument('-q', "--quiet", required=False, action='store_false', help="""Disable the ability of the program to print message on the terminal. (Optionnal) """, )
    parser.add_argument('-o', "--output", required=False, help="""Output name for the source code which will be created then compiled. Default value is "./firewall" (Optionnal) """, )
    # Template to display tool version
    parser.add_argument('-v', '--version', action='version', help='print the version and exit')
    args = vars(parser.parse_args())
    return args

if __name__ == '__main__':
    #Getting args from user
    args = getOptions()
    exampleCode = r'''
#include <stdio.h>
int main() {
    for(int i=0;i<5;i++) {
        printf("Testing %d\n",i);
    }
    return 0;
}
        '''
    canIPrintThisMessage = args['quiet']
    print(canIPrintThisMessage)
    if args['output'] is None:
        compiledFileName = './firewall'
    else:
        compiledFileName = args['output']
    sourceCodeFileName = writeSourceCode(exampleCode)
    returnValue = compileSourceCode(sourceCodeFileName,compiledFileName,canIPrintThisMessage)
    if returnValue == 0:
        executeAndReadCompiledProgram(compiledFileName,canIPrintThisMessage) # Run the compiled programm










