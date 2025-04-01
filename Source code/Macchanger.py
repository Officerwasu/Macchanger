#!/usr/bin/env python3
import subprocess
import optparse
import re
import random

def Macchanger(interface, mac_addr):
    print("[!]You selected " + interface)
    print("[+]Changing MAC address for " + interface + " to " + mac_addr)
    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", mac_addr])
    subprocess.run(["ifconfig", interface, "up"])

def theparser():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address for")
    parser.add_option("-m", "--mac", dest="mac_addr", help="New MAC address")
    parser.add_option("-r", "--random", action="store_true", dest="random_mac", help="Generate a random MAC address")  
    (parsoptions, parsarguments) = parser.parse_args()
    if not parsoptions.interface:
        parser.error("[X]You did not specify an interface, use --help for more info")
    elif not parsoptions.mac_addr and not parsoptions.random_mac: 
        parser.error("[X]Please enter a MAC address or use --random, use --help for more info")
    return parsoptions

def readmac(interface):
    check = subprocess.check_output(["ifconfig", interface])
    check = check.decode('utf-8')
    check_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", check)
    if check_result:
        return check_result.group(0)
    else:
        print("[x]MAC address not found.")

def generate_random_mac():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

parsoptions = theparser()

macnow = readmac(parsoptions.interface)
print("Mac Before = ", macnow)

if parsoptions.random_mac:
    random_mac = generate_random_mac()
    Macchanger(parsoptions.interface, random_mac)
    parsoptions.mac_addr = random_mac 
else:
    Macchanger(parsoptions.interface, parsoptions.mac_addr)

macnow = readmac(parsoptions.interface)
if macnow == parsoptions.mac_addr:
    print("[✔️] MAC address was sucessfully changed to ", macnow)
else:
    print("[x] MAC address did not get changed.")
