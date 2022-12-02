#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/icmp.h>
#include <netinet/in.h>
#include <bpf/bpf_helpers.h>

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

/*
            if (tcp->dest == ntohs(80)) { // Check if it is TCP port 80
                  return XDP_DROP;
            }
*/

/*
            if (udp->dest == ntohs(80)) { // Check if it is UDP port 80
                  return XDP_DROP;
            }
*/

char _license[] SEC("license") = "GPL";
