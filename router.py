from tuntap import TunTap
tun = TunTap(nic_type="Tun", nic_name="hnet-testnet")
tun.config(ip="192.168.99.1", mask="255.255.255.0")
input()