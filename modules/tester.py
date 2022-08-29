import time
import re
import sys
from os import system
from modules.resulter import ResultHandler
from modules.initializer import Initializer

class Tester:
    def __init__(self):
        pass

    def chooser(self, type, command, router_name, input):
        type_tester = type['type'].lower() + "_tester"
        func = getattr(Tester, type_tester)
        response = func(self, command, router_name, type, input)
        return response

    def serial_tester(self, command, router_name, type, input):
        router = self.open_serial_connection(command, input)
        response = self.execute_serial_commands(router, command, router_name, input)
        self.close_connection(router)
        return response

    def ssh_tester(self, command, router_name, type, input):        
        router = self.open_ssh_connection(type, input)
        response = self.execute_ssh_commands(router[1], command, router_name, type, input)
        return response

    def open_serial_connection(self, command, input):
        router = Initializer().chooser(command['authentication'], input)
        return router

    def open_ssh_connection(self, command, input):
        router = Initializer().chooser(command, input)
        router[1].send('ubus call mnfinfo get_value \'{"key": "name"}\'\r')
        time.sleep(1)
        router_name = router[1].recv(-1).decode().split('\r\n')
        if input.device.upper() != router_name[-3].split(':')[-1].replace('"', "").replace(" ", "")[0:6]:
            print('Entered device and device connected doesn\'t match')
            sys.exit()
        if router is None:
            return router
        else:
            router[1].send('/etc/init.d/gsmd stop\r')
            time.sleep(1)
            router[1].send('socat /dev/tty,raw,echo=0,escape=0x03 ' + str(router[2]) + ',raw,setsid,sane,echo=0,nonblock ; stty sane\r')
            time.sleep(1)
            i = router[1].recv(-1)
            return router

    def execute_serial_commands(self, router, command, router_name, input):
        response = []
        result = ResultHandler()
        try:
            router.write(b'ATE1\r')
            cmd_count = 0
            for cmd in command['commands']:
                attempts = 0
                success = False
                while attempts < 5 and not success:
                    try:
                        result.info(router_name, str(len(command['commands'])))
                        print(cmd['command'] + '\n')
                        msg = self.send_serial_command(cmd, router)
                        response.append(self.send_serial_result(msg, cmd, result))
                        time.sleep(1)
                        success = True
                    except (IndexError, OSError):
                        attempts += 1
                        time.sleep(10)
                        print('Error retrying attempt = ' + str(attempts))
                        router.close()
                        if not self.open_serial_connection(command, input) is False:
                            router = self.open_serial_connection(command, input)
                        if attempts == 5:
                            print("Connection lost")
                            response.append('Connection lost')
                            return response
            return response
        except FileExistsError:
            pass

    def execute_ssh_commands(self, router, command, router_name, type, input):
        response = []
        result = ResultHandler()
        test_result = '0'
        for cmd in command['commands']:
            attempts = 0
            success = False
            while attempts < 5 and not success:
                try:
                    result.info(router_name, str(len(command['commands'])))
                    print(cmd['command'] + '\n')
                    msg = self.send_ssh_command(cmd, router)
                    response.append(self.send_ssh_result(msg, cmd, result))
                    success = True
                    time.sleep(1)
                except (IndexError, OSError):
                    attempts += 1
                    print('Error retrying attempt = ' + str(attempts))
                    if not self.open_ssh_connection(type, input) is None:
                        router = self.open_ssh_connection(type, input)[1]
                    if attempts == 5:
                        print("Connection lost")
                        response.append('Connection lost')
                        return response
        return response

    def send_serial_command(self, cmd, router):
        if len(cmd['arguments'][0])>1:
            router.write(str(cmd['command'] + '\r').encode())
            time.sleep(1)
            for arg in cmd['arguments']:
                router.write(str(arg).encode() + b'\r')
                time.sleep(1)
            router.write(chr(26).encode())
        else:
            router.write((str(cmd['command']) + '\r').encode())
            time.sleep(1)
        msg = self.serial_response_timeout(router)
        return msg
                    
    def send_ssh_command(self, cmd, router):
        if len(cmd['arguments'][0])>1:
            router.send(cmd['command'] + '\r')
            time.sleep(1)
            for arg in cmd['arguments']:
                router.send(arg + '\r')
                time.sleep(1)
            router.send(chr(26).encode())
            time.sleep(1)
        else:
            router.send(cmd['command'] + '\r')
            time.sleep(1)
        msg = self.ssh_response_timeout(router)
        return msg

    def serial_response_timeout(self, router):
        timeout = time.time()+180
        while time.time()<timeout:
            txt = router.read()
            time.sleep(1)
            waiting_byte = router.inWaiting()
            txt += router.read(waiting_byte)
            if txt and ((b'\r\n\r\n' in txt) or (b'\r\r\n' in txt)):
                msg = txt.decode().split("\r\n")
                break
            else:
                msg = 'Timeout'
        return msg

    def send_serial_result(self, msg, cmd, result):
        try:
            if msg[-2] == cmd['expects']:
                test_result = True
                results = result.results_pass(cmd['command'], msg[-2], cmd['expects'], test_result)
            else:
                test_result = False
                results = result.results_fail(cmd['command'], msg[-2], cmd['expects'], test_result)
        except IndexError:
            pass
        return results

    def ssh_response_timeout(self, router):
        timeout = time.time()+180
        while time.time()<timeout:
            text = router.recv(-1)
            if text and (b'\n\n\n' in text):
                msg = text.decode().split('\n\n\n')[-1].replace('\n', '')
                break
            else:
                msg = 'Timeout'
        return msg

    def send_ssh_result(self, msg, cmd, result):
        if msg == cmd['expects']:
            test_result = True
            return result.results_pass(cmd['command'], msg, cmd['expects'], test_result)
        else:
            test_result = False
            return result.results_fail(cmd['command'], msg, cmd['expects'], test_result)

    def close_connection(self, router):
        router.close()
