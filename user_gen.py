#!/usr/bin/env python3

import argparse
import json

def expand_ip_range(ip_range):
    if '-' in ip_range:
        start_ip, last_octet_end = ip_range.split('-')
        start_ip_parts = start_ip.split('.')
        ip_addresses = [f"{'.'.join(start_ip_parts[0:3])}.{i}" for i in range(int(start_ip_parts[3]), int(last_octet_end) + 1)]
    else:
        ip_addresses = [str(ip) for ip in ipaddress.IPv4Network(ip_range)]
    return ip_addresses

def main():
    parser = argparse.ArgumentParser(description='Create a JSON structure with user data.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--usernames', nargs='+', help='A space-separated list of usernames')
    group.add_argument('--usernames-file', help='A file containing a list of usernames, one per line')
    parser.add_argument('--iprange', required=True, help='IP range (e.g., 192.168.0.0-100 or 192.168.0.0/24)')
    parser.add_argument('--outputfile', required=True, help='Name of the output JSON file')

    args = parser.parse_args()

    if args.usernames_file:
        with open(args.usernames_file, 'r') as f:
            args.usernames = [line.strip() for line in f]

    ip_addresses = expand_ip_range(args.iprange)

    if len(args.usernames) > len(ip_addresses):
        raise ValueError("The IP range does not contain enough addresses for all users")

    users = [
        #{"username": username, "ip_address": ip_address, "user_type": args.usertype}
        {"username": username, "ip_address": ip_address}
	for username, ip_address in zip(args.usernames, ip_addresses)
    ]

    with open(args.outputfile, 'w') as f:
        json.dump(users, f, indent=4)
    print("Output saved to file: %s" % args.outputfile)

if __name__ == '__main__':
    main()
