class ResultHandler:

    def results_pass(self, full_command, message):
        response = ('Command: ' + full_command + ' Message: ' + message + ' Test: Passed\n')
        print('Command: ' + full_command + ' Message: ' + message + ' Test: Passed')
        return response

    def results_fail(self, full_command, message, expects):
        response = ('Command: ' + full_command + ' Message: ' + message + ' Test: Failed Expected: ' + expects)
        print('Command: ' + full_command + ' Message: ' + message + ' Test: Failed Expected: ' + expects)
        return response

