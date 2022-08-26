from modules.configuration_handler import ConfigHandler
from modules.initializer import Initializer
from modules.write_to_file import WriteToFile
from modules.tester import Tester
import time
import argparse

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-IP', type=str, help="Devices SSH connection IP address", required=False)
    parser.add_argument('-u', type=str, help="Devices SSH connection username", required=False)
    parser.add_argument('-psw', type=str, help="Devices SSH connection password", required=False)
    parser.add_argument('-b', type=int, help="Devices Serial connection baud rate", required=False)
    parser.add_argument('-port', type=str, help="Devices connection port", required=False)
    parser.add_argument('device', type=str, help="Device name for script to test it")
    args = parser.parse_args()
    return args

command = ConfigHandler()
input = arg_parser()
router_name = input.device.upper()
response = Tester().chooser(command.get_param(router_name)['authentication'], command.get_param(router_name), router_name, input)
WriteToFile().writetofile(response, router_name)
