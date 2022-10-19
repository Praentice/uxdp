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
sudo apt install linux-perf
sudo apt install linux-headers-$(uname -r)
sudo apt install bpftool
sudo apt install tcpdump
export PATH=$PATH:/usr/sbin #Fix bug when bpftool is not found
```

```
pip install -r requirements.txt
```
### Running the tool
```commandline
Nothing yet.
```
## Documentation
### Syntax
./main.py (allow ; deny ; limit) on (1-65535 ; 80,443 ; 80-100 ; any) from (any ; 192.168.1.1 ; 192.168.1.0/24 ; 192.168.1.0-10 ; 192.168.1.10,192.168.1.11)

| Keyword                   | Explanation                                                                              |
|---------------------------|------------------------------------------------------------------------------------------|
| Allow                     | Allow access to a given port                                                             |
| Limit                     | Limit access to a given port                                                             |
| Deny                      | Deny access to a given port                                                              |
| 1-65535                   | Any network port between 1 and 65535 included                                            |
| 80, 443                   | Apply the rule on the network port 80 (HTTP) and 443 (HTTPS)                             |
| 80-100                    | Apply the rule on the network port 80 to the network port 100                            |
| 192.168.1.1               | Apply the rule to the 192.168.1.1 ip address only                                        |
| 192.168.1.0/24            | Apply the rule to the network subnet 192.168.1.0/24                                      |
| 192.168.1.0-10            | Apply the rule to all the ip address from 192.168.1.1 to 192.168.1.10 included           |
| 192.168.1.10,192.168.1.11 | Apply the rule to the 192.168.1.10 and 192.168.1.11 ip address                           |
| any                       | Apply the rule to all of the IP address or all of the network port based on its position |

#### Examples commands

| Command                                 | Explanation                                                                         |
|-----------------------------------------|-------------------------------------------------------------------------------------|
| ./main.py limit 80 from any             | Limit access to the network port number 80 (HTTP) from any IP address               |
| ./main.py allow 22 from 192.168.1.1     | Allow access to the network port number 22 (SSH) from 192.168.1.1                   |
| ./main.py allow 443 from 192.168.1.0/24 | Allow access to the network port number 443 (HTTPS) from the 192.168.1.0/24 network |
|                                         |                                                                                     |

### Optional flags
| Flag        | Description                          |
|-------------|--------------------------------------|
| -q/--quiet  | Disable the ability of the program to print message on the terminal.                      |
| -o/--output | Output name for the source code which will be created then compiled. Default value is "./firewall"  |                                     
## Credits

This tool is provided for free under GNU License.


