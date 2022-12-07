#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/icmp.h>
#include <netinet/in.h>
#include <bpf/bpf_helpers.h>

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
          if ((void*)tcp + sizeof(*tcp) <= data_end) { // Check if TCP packet isn't 
          
            // Begin section of generated code
            return XDP_PASS; // Fill here with dynamic code
            // End section of generated code
            
          }
          break;
        }

        case(IPPROTO_UDP): // If UDP is used as the transport protocol
        {
          struct tcphdr *udp = (void*)ip + sizeof(*ip); 
          if ((void*)udp + sizeof(*udp) <= data_end) { // Check if UDP packet isn't malformed

            // Begin section of generated code
            return XDP_PASS; // Fill here with dynamic code
            // End section of generated code

          }
          break;
        }

        case(IPPROTO_ICMP): // If ICMP is used as the transport protocol
        {
          struct icmphdr *icmp = (void*)ip + sizeof(*ip); 
          if ((void*)icmp + sizeof(*icmp) <= data_end) { // Check if the ICMP packet isn't malformed

            // Begin section of generated code
            return XDP_PASS; // Fill here with dynamic code
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


// MODULE_PORT_DEST = Module for TCP port dest : (PROTOCOL->dest == ntohs(PORT_DEST) // COMMENT
// MODULE_PORT_SRC = Module for TCP one port src : (PROTOCOL->src == ntohs(PORT_DEST) // COMMENT
// MODULE_PORT_SRC_RANGE = Module for TCP range port src : ((PROTOCOL->src >= ntohs(PORT_RANGE_MIN)) && (PROTOCOL->src <= ntohs(PORT_RANGE_MAX)) // COMMENT

// MODULE_IP_SRC = Module for IP address source only (One address and several) : (iphdr->src == IP_ADDR_SRC)
// MODULE_IP_SRC_NETWORK = Module for IP address source only (Network mask) : (is_ip_address_in_network(iphdr->src,NETIP,NETMASK))

// MODULE_PORT_DEST = Module for IP address destination only (One address and several) : (iphdr->dest == IP_ADDR_DEST)
// MODULE_PORT_DEST_NETWORK = Module for IP address destination only (Network mask) : (is_ip_address_in_network(iphdr->dest,NETIP,NETMASK))

/*
            if (MODULE_PORT_DEST && MODULE_PORT_SRC)) { // Check if it is TCP port PORT_DEST
              if (MODULE_IP_SRC && MODULE_IP_DEST) {
                  return XDP_PASS;
              }
            }
*/

/* For only one port dest in TCP
            if (tcp->dest == ntohs(PORT_DEST)) { // Check if it is TCP port PORT_DEST
                  return XDP_PASS;
            }
*/

/* For port dest and port src  in TCP
            if ((tcp->dest == ntohs(PORT_DEST)) && ((tcp->src >= ntohs(PORT_RANGE_MIN)) && (tcp->src <= ntohs(PORT_RANGE_MAX))) { // Check if it is TCP port 80
                  return XDP_PASS;
            }
*/

/* For only port dest in TCP
            if (tcp->dest == ntohs(PORT_DEST)) { // Check if it is TCP port PORT_DEST
                  return XDP_PASS;
            }
*/

/*
            if (udp->dest == ntohs(80) &&) { // Check if it is UDP port 80
                  return XDP_PASS;
            }
*/

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
