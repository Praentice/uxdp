# XUFW (XDP Uncomplicated Firewall)
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
### Optional flags
| Flag        | Description                          |
|-------------|--------------------------------------|
| -q/--quiet  | Disable the ability of the program to print message on the terminal.                      |
| -o/--output | Output name for the source code which will be created then compiled. Default value is "./firewall"  |                                     
## Credits

This tool is provided for free under GNU License.


