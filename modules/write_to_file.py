class WriteToFile():
    def writetofile(self, response):
        result_file = open("results/result.txt", "w")
        for element in response:
            result_file.write(element)
        result_file.close()