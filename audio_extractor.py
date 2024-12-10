import dpkt
import logging

logging.basicConfig(
    filename="../logs/audio_extractor.log", 
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def extract_audio(pcap_file, output_file):
    with open(pcap_file, "rb") as f:
        pcap = dpkt.pcap.Reader(f)
        with open(output_file, "wb") as audio_out:
            for ts, buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)
                ip = eth.data
                udp = ip.data
                audio_out.write(udp.data)


if __name__ == "__main__":
    import os
    os.makedirs("../audio", exist_ok=True)

    extract_audio("../captures/rtp_packets.pcap", "../audio/call_audio.raw")
