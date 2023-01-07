# UXDP (Uncomplicated XDP)
This CLI tool allows you to easily configure the XDP firewall on your server.
## Install the dependencies
First, do the following commands on a Debian virtual machine: 
```commandline
apt install sudo #Launch this command as root user
sudo apt update && sudo apt upgrade
sudo apt install git
git clone --recurse-submodules https://github.com/xdp-project/xdp-tutorial
sudo apt install clang llvm libelf-dev libpcap-dev gcc-multilib build-essential
sudo apt install linux-headers-$(uname -r)
sudo apt install python3 python3-pip
```
Then, install the required modules for the Python script : 
```
pip install -r requirements.txt
```
### Running the tool
You need to use sudo to run this tool.
```bash
sudo python3 /path/to/repo/uxdp.py
```
## Documentation
### Syntax


| Keyword                   | Explanation                                                                              |
|---------------------------|------------------------------------------------------------------------------------------|
| enable                    | enable the firewall                                                           |
| disable                      | disable the firewall                                                             |
| allow ARGS                    | Allow access to a given port                                                             |
| deny ARGS                     | Deny access to a given port                                                              |
| limit ARGS                     | Limit access to a given port                                                             |
|delete RULE/NUM |delete RULE|
|reload|reload firewall|
|reset|reset firewall|
|status|show firewall status|
|status numbered|show firewall status as a numbered list of RULES|
|version| display informations|

If you run the uxdp.py script with the action "allow", "deny" or "limit", you need to issue the following arguments : 



| Required Flag        | Description                          |
|-------------|--------------------------------------|
| -proto  | Choose the transport protocol to filter in our rule  |
| -interface | Choose the network interface on which the rule will be applied|
| -ipsrc | Choose the source ip address to filter in our rule|

| Optional Flag        | Description                          |
|-------------|--------------------------------------|
| -ipdst | Choose the destination ip address  to filter in our rule|firewall"  |     
|-comments|Add a comment to the rule|
|-portdst|Choose the destination port to filter in our rule|       
|-portsrc|Choose the source port to filter in our rule|   
|-limit|Put a rate limit on the packet which match the rule|

Here's some example of command you can run with this script.

| Command                                 | Explanation                                                                         |
|-----------------------------------------|-------------------------------------------------------------------------------------|
| sudo python3 /uxdp.py allow -proto=TCP -interface=eth0 -ipsrc=0.0.0.0/0 -comments=Allow-HTTP-Access -portdst=80 | Allow packets to the HTTP (80) port from anywhere               |
| sudo python3 /uxdp.py allow -proto=TCP -interface=eth0 -ipsrc=192.168.1.0/24 -comments=Allow-SSH-Access -portdst=22 | Allow packets to the SSH (22) port from the subnet 192.168.1.0/24.               |
| sudo python3 /uxdp.py allow -proto=TCP -interface=eth0 -ipdst=192.168.1.1/32 -ipsrc=192.168.1.0/24 -comments=Allow-FTP-Access -portdst=20-21 -portsrc=40000-50000 | Allow packets to the FTP (20 and 21) port from the subnet 192.168.1.0/24 only on the IP address 192.168.1.1 and from a source port which is included in the range 40000 to 50000.               |

## Credits

This tool is provided for free under GNU License.


