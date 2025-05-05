# Linux Macchanger (Python)

A command-line tool to randomize or set MAC addresses on Linux network interfaces.

## Features

* Random MAC address generation.
* Custom MAC address setting.

## Prerequisites

* Linux
* Python 3
* `sudo` privileges
* ifconfig(net-tools)

## Installation

1.  Download the script.
2.  Make it executable (`chmod +x macchanger.py`).
3.  (Optional) Move to a directory in your PATH.

## Usage

For help
sudo python3 Macchanger.py --help 

sudo Macchanger.py -i <interface> [-r | -m <MAC_ADDRESS>]

or

sudo python3 Macchanger.py -i <interface> [-r | -m <MAC_ADDRESS>]
