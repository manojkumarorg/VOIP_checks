import requests
import logging

logging.basicConfig(
    filename="../logs/get_location.log", 
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_ip_location(ip_address):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    data = response.json()
    return data


if __name__ == "__main__":
    ip = "8.8.8.8"  # Replace with actual IP from SIP packet
    location = get_ip_location(ip)
    print(f"IP: {ip}, Location: {location}")

