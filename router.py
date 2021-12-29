#!/usr/bin/env python3

from tuntap import TunTap
import socket
import sys

# -------------PARAMS-------------- #

HOST = '10.0.157.101' # (socket.gethostbyname(socket.gethostname())
PORT = 65432
NIC_NAME = "hnet-testnet"
IFACE_IP = "192.168.99.1" # Default hnet tun/tap local ip

# --------------------------------- #

# tuntap check for win os
if sys.platform.startswith("win"):
    tunTapAllow = False
else:
    tunTapAllow = True

# Init tuntap for tunnel
if tunTapAllow:
    tun = TunTap(nic_type="Tun", nic_name=NIC_NAME)
    tun.config(ip=IFACE_IP, mask="255.255.255.0")
else:
    pass

# Packet stream buffering
def hBuffer():
    pass

# Tcp tunnel
def tcp_handler():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                        while True:
                            data = conn.recv(1024)
                            if tunTapAllow:
                                tun.write(data)
                            if not data:
                                break
                            conn.sendall(data)
    except KeyboardInterrupt:
        tun.close()

# Udp tunnel
def udp_handler():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((HOST, PORT))
            while True:
                data, addr = s.recvfrom(8)
                print(data)
                if tunTapAllow:
                    tun.write(data)
                #s.sendto(data, ("178.41.16.171", PORT))
    except KeyboardInterrupt:
        tun.close()

udp_handler()