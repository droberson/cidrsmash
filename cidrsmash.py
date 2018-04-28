#!/usr/bin/env python3

"""
  cidrsmash.py -- by Daniel Roberson @dmfroberson           April/2018

This script takes an input file or reads from stdin a list of IP
addresses and condenses them into networks in CIDR notation.

Examples:

$ cat ips | ./cidrsmash.py -m 24
10.0.0.0/24
10.0.1.0/24
...

$ ./cidrsmash.py -m 16 ips
10.0.0.0/16

TODO: more intuitive docstrings
TODO: IPv6
"""

import os
import sys
import struct
import socket
import argparse


def valid_ip_address(ip_address):
    """ valid_ip_address() -- Validate an IP address
    """
    try:
        socket.inet_aton(ip_address)
    except socket.error:
        return False
    return True


def ip_to_long(ip_address):
    """ ip_to_long() -- Convert human readable IP address to integer
    """
    tmp = socket.inet_aton(ip_address)
    return struct.unpack("!L", tmp)[0]


def long_to_ip(ip_address):
    """ long_to_ip() -- Convert IP integer IP addresses to human
                     -- readable string.
    """
    return socket.inet_ntoa(struct.pack("!L", ip_address))


def network_from_cidr(ip_address, cidrmask):
    """ network_from_cidr() -- Calculates network address via CIDR mask
    """
    ip_addr = ip_to_long(ip_address)
    mask = (0xffffffff << 32 - int(cidrmask)) & 0xffffffff
    return long_to_ip(mask & ip_addr)


def parse_cli():
    """ parse_cli() -- parses CLI input with argparser
    """
    description = "example: cidrsmash.py -m 27"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("infile",
                        nargs="?",
                        default=sys.stdin,
                        help="Input file. Default is stdin.")
    parser.add_argument("-m",
                        "--mask",
                        required=False,
                        default=24,
                        help="CIDR mask: 1-32")
    args = parser.parse_args()

    # Make sure CIDR mask is between 1 and 32
    if int(args.mask) < 0 or int(args.mask) > 32:
        print("CIDR mask out of range: %s" % args.mask)
        exit(os.EX_USAGE)

    return args


def main():
    """ main() -- main function
    """
    args = parse_cli()

    ips = []
    networks = []

    # Read from infile or stdin
    if args.infile == sys.stdin:
        infile = sys.stdin
    else:
        infile = open(args.infile, "r")

    # Read infile into ips[]
    for line in infile:
        line = line.rstrip()

        # Skip blank lines and comments
        if line == "" or line.startswith("#") or line.startswith(";"):
            continue
        # Only add valid IPv4 addresses
        if valid_ip_address(line) is True:
            ips.append(line)
    infile.close()

    for ip_address in ips:
        networks.append(
            str(network_from_cidr(ip_address, args.mask)) + \
                "/" + \
                str(args.mask))

    # Print unique list
    for network in set(networks):
        print(network)


if __name__ == "__main__":
    main()
