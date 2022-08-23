import serial
import paramiko
import sys

class Initializer:
    def router_info(self):
        if sys.argv[-1] == "script.py":
            print("Enter router name as argument")
            sys.exit()
        router_name = sys.argv[-1].upper()
        return router_name

    def initializer(self, init_info):
        if init_info['type'] == "serial":
            router = serial.Serial(
                init_info['port'],
                init_info['baud_rate'],
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1,
                rtscts=False,
                dsrdtr=False,
                write_timeout=1)
        elif init_info['type'] == "SSH":
            addr = init_info['address']
            username = init_info['username']
            password = init_info['password']
            router = paramiko.SSHClient()
            router.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            router.connect(addr, 22, username, password)
        return router
