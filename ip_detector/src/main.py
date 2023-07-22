import os
import pathlib
from typing import Optional

import requests
from mcqueue import Queue
from mclogging import setup_logs, logger

IP_FILE_PATH = pathlib.Path("/ip/ip.txt")
IP_API_URL = "https://api.ipify.org"


def get_old_ip() -> Optional[str]:
    if not os.path.isfile(IP_FILE_PATH):
        return None
    with open(IP_FILE_PATH, "r") as ip_file:
        return ip_file.read()


def save_new_ip(new_ip: str) -> None:
    with open(IP_FILE_PATH, "w") as ip_file:
        ip_file.write(new_ip)
        ip_file.truncate()


def announce_new_ip(new_ip: str) -> None:
    with Queue() as q:
        q.publish(f"Our IP address has changed! {new_ip}")
    logger.info(f"New IP address detected: {new_ip}")


def get_current_ip() -> str:
    current_ip_request = requests.get(IP_API_URL)
    if current_ip_request.status_code >= 400:
        raise Exception("Could not get current IP address")
    return current_ip_request.text


if __name__ == "__main__":
    setup_logs("ip_detector")
    logger.info("Searching for new IP address...")
    old_ip = get_old_ip()
    current_ip = get_current_ip()
    if old_ip != current_ip:
        announce_new_ip(current_ip)
        save_new_ip(current_ip)
