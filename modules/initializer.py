from xml.dom.minidom import Attr
import serial
import paramiko
import sys
import socket

class Initializer:
    def __init__(self):
        pass

    def chooser(self, init_info, input):
        try:
            router = init_info['type'].lower() + "_initializer"
            func = getattr(Initializer, router)
            response = func(self, init_info, input)
            return response
        except AttributeError:
            pass

    def serial_initializer(self, init_info, input):
        try:
            if input.port:
                port = input.port
            elif init_info['port']:
                port = init_info['port']
            else:
                port = init_info['default_port']
            if input.b:
                baud_rate = input.b
            elif init_info['baud_rate']:
                baud_rate = init_info['baud_rate']
            else:
                baud_rate = init_info['default_baud_rate']
            router = serial.Serial(
                port,
                baud_rate,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1,
                rtscts=False,
                dsrdtr=False,
                write_timeout=1)
            return router
        except (FileNotFoundError, serial.serialutil.SerialException):
            router = False
            return router
    
    def ssh_initializer(self, init_info, input):
        if input.IP:
            addr = input.IP
        elif init_info['address']:
            addr = init_info['address']
        else:
            addr = init_info['default_address']
        if input.u:
            username = input.u
        elif init_info['username']:
            username = init_info['username']
        else:
            username = init_info['default_username']
        if input.psw:
            password = input.psw
        elif init_info['password']:
            password = init_info['password']
        else:
            password = init_info['default_password']
        router = paramiko.SSHClient()
        router.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            router.connect(addr, 22, username, password, timeout = 6)
            if input.port:
                port = input.port
            elif init_info['port']:
                port = init_info['port']
            else:
                port = init_info['default_port']
            shell = router.invoke_shell()
            return router, shell, port
        except paramiko.ssh_exception.AuthenticationException:
            print('Configured login information is incorrect')
            sys.exit()
        except paramiko.ssh_exception.NoValidConnectionsError:
            print('Configured IP address is incorrect')
            sys.exit()
        except TimeoutError:
            pass
        except socket.timeout:
            pass
