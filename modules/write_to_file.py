from datetime import datetime
import sys

class WriteToFile():
    def writetofile(self, response, router):
        now = datetime.now()
        filename = now.strftime("%Y-%m-%d_%H:%M:%S")
        try:
            result_file = open("results/" + router + "_" + filename  + ".csv", "w")
            result_file.write('Command,Expected,Response,Test\n')
            for element in response:
                result_file.write(element)
            result_file.close()
        except FileNotFoundError:
            print('results directory is missing')
