import socket
import dpkt
import logging

# Set up logging to debug and trace packet capture
logging.basicConfig(
    filename="../logs/network_sniffer.log", 
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def save_packet(packet, filename):
    """Save the packet to a file."""
    with open(filename, "ab") as f:
        f.write(packet)

def parse_packet(raw_data):
    """
    Parse packets to detect SIP and RTP traffic.
    Returns a tuple (packet_type, parsed_data), where packet_type is SIP/RTP/None.
    """
    try:
        eth = dpkt.ethernet.Ethernet(raw_data)
        if not isinstance(eth.data, dpkt.ip.IP):
            return None, None

        ip = eth.data
        if not isinstance(ip.data, dpkt.udp.UDP):
            return None, None

        udp = ip.data
        # SIP typically uses port 5060
        if udp.dport == 5060 or udp.sport == 5060:
            return "SIP", udp.data.decode(errors="ignore")
        # RTP typically uses dynamic UDP ports above 1024
        elif udp.dport > 1024 or udp.sport > 1024:
            return "RTP", udp.data
    except Exception as e:
        logging.error(f"Error parsing packet: {e}")
        return None, None

    return None, None


def sniff_packets():
    """
    Sniff network packets and filter for SIP and RTP traffic.
    Saves captured packets to ../captures/filtered_packets.pcap.
    """
    try:
        logging.info("Starting packet sniffing...")
        # Create a raw socket to capture all network packets
        sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

        # Capture and process packets in a loop
        while True:
            raw_data, addr = sniffer.recvfrom(65536)
            packet_type, parsed_data = parse_packet(raw_data)

            if packet_type == "SIP":
                logging.info(f"SIP packet captured from {addr}")
                save_packet(raw_data, "../captures/sip_packets.pcap")

            elif packet_type == "RTP":
                logging.info(f"RTP packet captured from {addr}")
                save_packet(raw_data, "../captures/rtp_packets.pcap")

    except KeyboardInterrupt:
        logging.info("Packet sniffing stopped.")
        print("\nPacket sniffing stopped.")
    except Exception as e:
        logging.error(f"Error during packet sniffing: {e}")


if __name__ == "__main__":
    # Create necessary directories if they don't exist
    import os
    os.makedirs("../captures", exist_ok=True)
    os.makedirs("../logs", exist_ok=True)

    sniff_packets()
