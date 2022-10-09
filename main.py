#!/usr/bin/python3
import argparse
import sys
import os
VERSION=1.0

def exampleFunction(test1,test2):
    return test1,test2

def getOptions():
    parser = argparse.ArgumentParser(add_help=True, formatter_class=argparse.RawTextHelpFormatter,description=
    """
    XUFW                  
    This CLI tool allows you to easily configure the XDP firewall on your server
    """,
    epilog=
    """
    This tool is provided for free under GNU Licence.
    """,
    )
    parser.version = "The current version is {}".format(VERSION)
    # Template for mandatory arguments
    parser.add_argument('-n1', "--nothing1", required=True,help="""Nothing here. (Mandatory)""",nargs=*)
    # Template for optionnal arguments
    parser.add_argument('-n2', "--nothing2", required=False,help="""SNothing here. (Optionnal)""", )
    # Template to display tool version
    parser.add_argument('-v', '--version', action='version', help='print the version and exit')
    args = vars(parser.parse_args())
    return args

if __name__ == '__main__':
    #Getting args from user
    args = getOptions()







