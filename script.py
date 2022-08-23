from modules.configuration_handler import ConfigHandler
from modules.initializer import Initializer
from modules.write_to_file import WriteToFile
from modules.tester import Tester
import time

command = ConfigHandler()
router_name = Initializer().router_info()
router = Initializer().initializer(command.get_param(router_name)['authentication'])
# response = Tester().serial_tester(command.get_param(router_name), router, router_name)
# WriteToFile().writetofile(response, router_name)
stdin, stdout, stderr = router.exec_command('/etc/init.d/gsmd stop')
stdin.close()
print(stdout.readlines())
stdin, stdout, stderr = router.exec_command('socat /dev/tty,raw,echo=0,escape=0x03 /dev/ttyUSB3,raw,setsid,sane,echo=0,nonblock ; stty sane\r')
stdin.close()
print(stdout.readlines())
stdin, stdout, stderr = router.exec_command('ls')
time.sleep(5)
stdin.close()
for line in stdout.read().splitlines():
    print(line)
