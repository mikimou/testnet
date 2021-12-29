#!/usr/bin/env python3

from logging import exception
from os import kill
from tuntap import TunTap
import socket

HOST = '10.0.157.101' # (socket.gethostbyname(socket.gethostname())
PORT = 65432


tun = TunTap(nic_type="Tun", nic_name="hnet-testnet")
tun.config(ip="192.168.99.1", mask="255.255.255.0")

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
                            tun.write(data)
                            if not data:
                                break
                            conn.sendall(data)
    except KeyboardInterrupt:
        tun.close()

def udp_handler():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((HOST, PORT))
            while True:
                data, addr = s.recv(1024)
                tun.write(data)
                if not data:
                    break
                s.sendto(data, "178.41.16.171", PORT)
    except KeyboardInterrupt:
        tun.close()