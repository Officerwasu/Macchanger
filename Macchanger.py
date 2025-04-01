#!/usr/bin/env python3

import subprocess
import random
import re
import optparse

def generate_random_mac():
    """Generates a random MAC address."""
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def is_valid_mac(mac_address):
    """Checks if a MAC address is valid."""
    return bool(re.match(r'^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$', mac_address))

def change_mac(interface, mac_address):
    """Changes the MAC address of a network interface."""
    try:
        subprocess.run(["ifconfig", interface, "down"], check=True)
        subprocess.run(["ifconfig", interface, "hw", "ether", mac_address], check=True)
        subprocess.run(["ifconfig", interface, "up"], check=True)
        print(f"[+] MAC address of {interface} changed to {mac_address} successfully.")

    except subprocess.CalledProcessError as e:
        print(f"[-] Command execution failed: {e}")
        if "Operation not permitted" in str(e):
            print("[-] Permission denied. Try running as root (sudo).")
        elif "No such device" in str(e):
            print(f"[-] Interface '{interface}' not found.")
        else:
            print("[-] Check interface name, MAC address, and permissions.")

    except FileNotFoundError:
        print("[-] ifconfig command not found. Ensure net-tools is installed.")

    except Exception as e:
        print(f"[-] An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    parser.add_option("-r", "--random", action="store_true", dest="random_mac", help="Generate a random MAC address")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        if options.random_mac:
            print(generate_random_mac()) # only print the mac address if -r is given.
        else:
            parser.error("[-] Please specify an interface, use --help for more info.")

    interface = options.interface

    if options.random_mac:
        mac_address = generate_random_mac()
        print(f"[+] Generating random MAC: {mac_address}")
    elif options.new_mac:
        mac_address = options.new_mac
        if not is_valid_mac(mac_address):
            print("[-] Invalid MAC address format.")
            exit(1)
    else:
        parser.error("[-] Please specify a new MAC address or use --random, use --help for more info.")

    print(f"[!] You selected {interface}")
    print(f"[+] Changing MAC address for {interface} to {mac_address}")
    change_mac(interface, mac_address)