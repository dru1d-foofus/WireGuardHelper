# WireGuard Provisioning Scripts

These scripts are used to facilitate the creation of WireGuard configuration files.

## user_gen.py
This script takes a list of usernames and an IP range (like 192.168.0.10-15 or 192.168.0.0/24) and creates the initial json structure that the second script uses.

```
usage: user_gen.py [-h] (--usernames USERNAMES [USERNAMES ...] | --usernames-file USERNAMES_FILE) --iprange IPRANGE --outputfile OUTPUTFILE
user_gen.py: error: the following arguments are required: --iprange, --outputfile
```

Example Usage:
```
python3 user_gen.py --usernames-file usernames.txt --iprange 127.0.0.10-20 --outputfile users.json
```

Example json Output:
```
[
    {
        "username": "dru1d",
        "ip_address": "127.0.0.10"
    },
    {
        "username": "test",
        "ip_address": "127.0.0.11"
    },
    {
        "username": "testadmin",
        "ip_address": "127.0.0.12"
    },
    {
        "username": "testuser",
        "ip_address": "127.0.0.13"
    }
]
```

## wireguard_gen.py
This script takes a json structure and creates WireGuard public/private keypairs and a user wg0.conf file that gets committed to a directory for distribution to the user. It also modifies the server's `/etc/wireguard/wg0.conf` and can even restart the WireGuard service. You will need elevated privileges to run this.

```
usage: wireguard_gen.py [-h] --inputfile INPUTFILE --endpoint ENDPOINT [--port PORT] --allowedips ALLOWEDIPS [--dryrun] [--restart] --publickey PUBLICKEY
wireguard_gen.py: error: the following arguments are required: --inputfile, --endpoint, --allowedips, --publickey
```

Example Usage:

This will conduct an initial dryrun and will not create any files/change any files.
```
python3 wireguard_gen.py --inputfile users.json --publickey test --allowedips 127.0.0.0/24 --dryrun
```

This will generate the user directories, make config changes.
```
python3 wireguard_gen.py --inputfile users.json --publickey test --allowedips 127.0.0.0/24 
```

This will make the configuration changes, generate the files, and restart the WireGuard service.
```
python3 wireguard_gen.py --inputfile users.json --publickey test --allowedips 127.0.0.0/24 --restart
```

Example json Output:
```
[
    {
        "username": "dru1d",
        "ip_address": "127.0.0.10/32",
        "public_key": "O5kktWdQZDYafRH5XhCXO3HYUZCixz7/9qMwt9+G5gA="
    },
    {
        "username": "test",
        "ip_address": "127.0.0.11/32",
        "public_key": "TZcSo4a8uZDef00p3lpYFP4WHSVgOmmki9ZR41lZjVk="
    },
    {
        "username": "testadmin",
        "ip_address": "127.0.0.12/32",
        "public_key": "2dso55lnw3cvHmPcILAMI/xjBaX6aSuxqUysccDC1BY="
    },
    {
        "username": "testuser",
        "ip_address": "127.0.0.13/32",
        "public_key": "qVSLIScnguR3+Mj9ClWhpMsbUQ0i2J8krMsrgxg3A3Q="
    }
]
```