from modules.configuration_handler import ConfigHandler
from modules.initializer import Initializer
from modules.write_to_file import WriteToFile
from modules.tester import Tester

command = ConfigHandler()
router = Initializer().initializer()
response = Tester().cmd_tester(command.get_param('TRM240'), router)
WriteToFile().writetofile(response)