#!/usr/bin/env python3

import argparse
import json
import os
import subprocess

def generate_wireguard_keys():
    private_key = subprocess.run(['wg', 'genkey'], capture_output=True, text=True).stdout.strip()
    public_key = subprocess.run(['wg', 'pubkey'], capture_output=True, input=private_key, text=True).stdout.strip()
    return private_key, public_key

def main():
    parser = argparse.ArgumentParser(description='Generate WireGuard keys and configuration from user data')
    parser.add_argument('--inputfile', required=True, help='Name of the input JSON file')
    parser.add_argument('--endpoint', required=True, help='WireGuard VPN server endpoint')
    parser.add_argument('--port', default=51820, help='WireGuard VPN server port')
    parser.add_argument('--allowedips', required=True, help='Allowed IP range for WireGuard VPN')
    parser.add_argument('--dryrun', action='store_true', help='Run the script without making any changes')
    parser.add_argument('--restart', action='store_true', help='Restart WireGuard service after changes')
    parser.add_argument('--publickey', required=True, help='WireGuard server public key')

    args = parser.parse_args()

    with open(args.inputfile, 'r') as f:
        users = json.load(f)

    for user in users:
        private_key, public_key = generate_wireguard_keys()
        #user['private_key'] = private_key
        user['public_key'] = public_key
        user['ip_address'] = user['ip_address'] + '/32'  # Append /32 to the IP address

        # Create directory for the user under user_config directory
        user_dir = os.path.join('user_config', user['username'])
        os.makedirs(user_dir, exist_ok=True)

        # Write the private key, public key, and user wg0.conf file to the user's directory
        with open(os.path.join(user_dir, 'private_key'), 'w') as f:
           f.write(private_key)
        with open(os.path.join(user_dir, 'public_key'), 'w') as f:
            f.write(public_key)
        with open(os.path.join(user_dir, 'wg0.conf'), 'w') as f:
            f.write(f"[Interface]\nPrivateKey = {private_key}\nAddress = {user['ip_address']}\n\n"
                     f"[Peer]\nPublicKey = {args.publickey}\n"
                     f"AllowedIPs = {args.allowedips}\nEndpoint = {args.endpoint}:{args.port}\nPersistentKeepalive = 25\n")

        print(f"## {user['username']}\n[Peer]\nPublicKey = {public_key}\nAllowedIPs = {user['ip_address']}")

        if not args.dryrun:
            with open('/etc/wireguard/wg0.conf', 'a') as f:
                f.write(f"## {user['username']}\n[Peer]\nPublicKey = {public_key}\nAllowedIPs = {user['ip_address']}\n")

    with open(args.inputfile.replace('.json', '_wg.json'), 'w') as f:  # Replace .json with _wg.json in the filename
        json.dump(users, f, indent=4)

    if args.restart and not args.dryrun:
        subprocess.run(['systemctl', 'restart', 'wg-quick@wg0'], check=True)

if __name__ == '__main__':
    main()
