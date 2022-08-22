import time
from modules.resulter import ResultHandler

class Tester:
    def cmd_tester(self, command, router):
        response = []
    
        for cmd in command[0]['commands']:
            if len(cmd['arguments'][0])>1:
                router.write(str(cmd['command'] + '\r').encode())
                time.sleep(0.5)
                router.write(str(cmd['arguments'][0]).encode() + b'\r')
                time.sleep(0.5)
                router.write(chr(26).encode())
            else:
                router.write((str(cmd['command']) + '\r').encode())
            msg = router.readall().decode().split("\r\n")
            if msg[-2] == cmd['expects']:
                if len(cmd['arguments'][0])>1:
                    response.append(ResultHandler().results_pass(cmd['command'], msg[-2]))
                    print(cmd['arguments'])
                else:
                    response.append(ResultHandler().results_pass(cmd['command'], msg[-2]))
            else:
                if len(cmd['arguments'][0])>1:
                    response.append(ResultHandler().results_fail(cmd['command'], msg[-2], cmd['expects']))
                    print(cmd['arguments'])
                else:
                    response.append(ResultHandler().results_fail(cmd['command'], msg[-2], cmd['expects']))
                

        router.close()
        return response
