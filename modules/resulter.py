from colorama import Fore, Style
from os import system

class ResultHandler:
    __passed_count = 0
    __failed_count = 0

    def __init__(self):
        pass

    def info(self, router, command_number):
        system('clear')
        print(Fore.BLUE + router)
        print(Style.RESET_ALL)
        print("Number of commands: " + command_number + "\n")

    def results_pass(self, full_command, message, expects, test_result):
        if test_result:
            self.__passed_count += 1
        else:
            self.__failed_count += 1
        full_command = full_command.replace("\"", "")
        response = (full_command + ',' + expects + ',' + message + ',Passed\n')
        print(Fore.GREEN + 'Passed: ' + str(self.__passed_count) + " " + Fore.RED + 'Failed: ' + str(self.__failed_count))
        print(Style.RESET_ALL)
        return response

    def results_fail(self, full_command, message, expects, test_result):
        if test_result:
            self.__passed_count += 1
        else:
            self.__failed_count += 1
        full_command = full_command.replace("\"", "")
        response = (full_command + ',' + expects + ',' + message + ',Failed\n')
        print(Fore.GREEN + 'Passed: ' + str(self.__passed_count) + " " + Fore.RED + 'Failed: ' + str(self.__failed_count))
        print(Style.RESET_ALL)
        return response
