import json
from subprocess import call, check_call, CalledProcessError

from config import Config

__author__ = "Jim Martens"


class Connection:
    """
    Manages the connection with the server.
    """
    def __init__(self):
        self._sshHost = None
        self._dataFile = None
        self._pathToDir = None
        self._pathToTool = None
        self._pathToData = None
        self._errorObject = None # type: CalledProcessError
        self.reload_config()

    def get_error_object(self):
        return self._errorObject
    
    def reload_config(self):
        config = Config()
        self._sshHost = config.get("SSH", "host")
        self._dataFile = config.get("Data", "file")
        self._pathToDir = config.get("Data", "path_to_dir")
        self._pathToTool = config.get("Data", "path_to_tool")
        self._pathToData = config.get("Data", "path_to_data")

    def send_print_data(self, print_amounts, printer):
        """
        Sends print data to the server.
        :param print_amounts: the effective print amounts for each material or sub material
        :type print_amounts: dict
        :param printer: the printer to be used for - well - printing
        :type printer: str
        :return True on success, False otherwise
        :rtype: bool
        """
        data = {
            "amounts": print_amounts,
            "printer": printer
        }
        json_data = json.dumps(data, separators=(',',':'))
        return self._send_to_server("print", "'" + json_data + "'")

    def synchronize_data(self):
        """
        Synchronizes the data.json with the authoritative server version.
        :return: Returns True on success, False otherwise
        :rtype: bool
        """
        try:
            check_call(["scp", self._sshHost + ":" + self._pathToData, self._dataFile])
            return True
        except CalledProcessError as cpe:
            self._errorObject = cpe
            return False

    def _send_to_server(self, command, data):
        """
        Performs the actual sending of data to the server.
        :param command:
        :type command: str
        :param data:
        :type data: str
        :return True on success, False otherwise
        :rtype:
        """
        try:
            check_call(["ssh", self._sshHost, "cd " + self._pathToDir + "; ./" + self._pathToTool, command, data])
            return True
        except CalledProcessError as cpe:
            self._errorObject = cpe
            return False
