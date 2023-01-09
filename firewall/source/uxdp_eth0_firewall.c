#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/udp.h>
#include <linux/icmp.h>
#include <netinet/in.h>
#include <bpf/bpf_helpers.h>
#include <stdio.h>

const int true = 1;
const int false = 0;

//Function to check if IP address is in network sub
int is_ip_address_in_network(uint32_t ip, uint32_t netip, uint32_t netmask){
  //uint32_t ip = ...; // value to check as a int value
  //uint32_t netip = ...; // network ip to compare with as a int value
  //uint32_t netmask = ...; // network ip subnet mask as a int value
  if ((netip & netmask) == (ip & netmask)) {
    return 1;
  }
    // is on same subnet...
  else {
    return 0;
  }
    // not on same subnet...
}

SEC("firewall")
int myxdpprogram(struct xdp_md *ctx) {
  void *data = (void *)(long)ctx->data;
  void *data_end = (void *)(long)ctx->data_end;
  // Dissecting the Ethernet Frame
  struct ethhdr *eth = data;

  // Does the size of the packet really fits as an Ethernet Frame
  if ((void*)eth + sizeof(*eth) <= data_end) { // Check if Ethernet Frame isn't malformed
    
    // Dissecting the IPv4 part
    struct iphdr *ip = data + sizeof(*eth);
    if ((void*)ip + sizeof(*ip) <= data_end) { // Check if IPv4 packet isn't malformed
      switch(ip->protocol) { // Switch case to determine the protocol
        case(IPPROTO_TCP): // If TCP is used as the transport protocol
        {
          struct tcphdr *tcp = (void*)ip + sizeof(*ip); 
          if ((void*)tcp + sizeof(*tcp) <= data_end) { // Check if TCP packet isn't malformed
          // Begin section of generated code
            if(is_ip_address_in_network(ip->daddr,ntohl(0xE0000000),ntohl(0xF0000000))){ // Check if TCP packet is multicast
              return XDP_PASS; //Change this line to 'return XDP_DROP;' to disable multicast
            }
            if ((tcp->dest == ntohs(80)) && (1)) { // Allow-HTTP-Access 
		          if (((is_ip_address_in_network(ip->saddr,ntohl(0x00000000),ntohl(0x00000000)))) && (1)) {
			          return XDP_PASS;
		          }
            }
//GENERATED_CODE_TCP
          // End section of generated code
          }
          break;
        }

        case(IPPROTO_UDP): // If UDP is used as the transport protocol
        {
          struct udphdr *udp = (void*)ip + sizeof(*ip); 
          if ((void*)udp + sizeof(*udp) <= data_end) { // Check if UDP packet isn't malformed
          // Begin section of generated code
          if (udp->dest == ntohs(68) || (udp->dest == ntohs(53))){ // Check if UDP datagram is DHCP
            return XDP_PASS; //Change this line to 'return XDP_DROP;' to disable DHCP
          }
//GENERATED_CODE_UDP
          // End section of generated code
          }
          break;
        }

        case(IPPROTO_ICMP): // If ICMP is used as the transport protocol
        {
          struct icmphdr *icmp = (void*)ip + sizeof(*ip); 
          if ((void*)icmp + sizeof(*icmp) <= data_end) { // Check if the ICMP packet isn't malformed
            // Begin section of generated code
            return XDP_PASS; //Change this line to 'return XDP_DROP;' to disable ICMP
            // End section of generated code
          }
          break;
        }

      }
    }
  }
  // Take a default action
  return XDP_DROP;

}
/*
// https://stackoverflow.com/questions/31040208/standard-safe-way-to-check-if-ip-address-is-in-range-subnet
uint32_t ip = ...; // value to check
uint32_t netip = ...; // network ip to compare with
uint32_t netmask = ...; // network ip subnet mask
if ((netip & netmask) == (ip & netmask))
    // is on same subnet...
else
    // not on same subnet...
*/


char _license[] SEC("license") = "GPL";
