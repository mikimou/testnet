#!/usr/bin/env python3

from tuntap import TunTap
import socket

tun = TunTap(nic_type="Tun", nic_name="hnet-testnet")
tun.config(ip="192.168.99.1", mask="255.255.255.0")

HOST = '10.0.157.101' # (socket.gethostbyname(socket.gethostname())
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(1024)
            tun.write(data)
            if not data:
                break
        except KeyboardInterrupt:
            tun.close()