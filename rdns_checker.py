#!/usr/bin/env python

import socket
import sys
import os

def get_banner(ip_address):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        s.connect((ip_address, 25)) # port 25
        banner = s.recv(1024)
        return banner
    except:
        return None

def get_rdns(ip_address):
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        return None


def ping_ip(ip_address):
    response = os.system("ping -c 1 -w2 " + ip_address + " > /dev/null 2>&1")
    if response == 0:
        return True
    else:
        return False

def write_log(log_file, ip_address, *args):
    with open(log_file, "a") as my_file:
        my_file.write("{ip} - {args}\n".format(ip=ip_address, args=map(str, args)))

def main():
     for i in range(0,255):
        # Define as '127.0.0.'
        ip_address = '127.0.0.' + str(i)

        ip_pingable = ping_ip(ip_address)
        if not ip_pingable:
            write_log("ip-down.txt", ip_address)
            continue

        banner = get_banner(ip_address)
        rdns = get_rdns(ip_address)

        if not banner:
            write_log("no-banner.txt", ip_address)
            continue

        if not rdns:
            write_log("no-rdns.txt", ip_address, banner)
            continue

        # check if rdns is in banner
        if rdns in banner:
            write_log("correct_rdns.txt", ip_address, banner, rdns)
        else:
            write_log("wrong_rdns.txt", ip_address, banner, rdns)


if __name__ == '__main__':
     main()