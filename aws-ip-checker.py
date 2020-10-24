import argparse
import json
from ipaddress import ip_address, ip_network

import requests

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--ipaddress", "-i", type=str, help="IP address to check", action="append", required=True)
ARGS = PARSER.parse_args()

def fetch_aws_json(url: str) -> str:
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()

    except requests.exceptions.HTTPError as err:
        print(f"[!] {err}")

def check_in_range(aws_json: str, target_ip: str):

    for address_prefix in aws_json["prefixes"]:
        subnet = ip_network(address_prefix["ip_prefix"])

        if ip_address(target_ip) in subnet:
            return address_prefix

if __name__ == "__main__":
    aws_json = fetch_aws_json('https://ip-ranges.amazonaws.com/ip-ranges.json')

    for ip in ARGS.ipaddress:
        result = check_in_range(aws_json, ip)
        if result:
            print(f"{ip} is in AWS region {result['region']} in subnet {result['ip_prefix']}")
        else:
            print(f"{ip} is not in an in AWS region")
