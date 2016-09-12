import json
from subprocess import CalledProcessError
import pexpect
import time

from config import Config
from ssh_dialog import SSHInput

__author__ = "Jim Martens"


class Connection:
    """
    Manages the connection with the server.
    """
    def __init__(self, ssh_input=None):
        self._sshHost = None
        self._dataFile = None
        self._pathToDir = None
        self._pathToTool = None
        self._pathToData = None
        self._sshInput = ssh_input # type: SSHInput
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
            process = pexpect.spawn(
                "ssh",
                [self._sshHost + ":" + self._pathToData, self._dataFile]
            )
            process.expect("oe@rzssh1.informatik.uni-hamburg.de's password:")
            time.sleep(0.1)
            process.sendline(self._sshInput.readline())
            time.sleep(2)
            process.expect(pexpect.EOF)
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
            process = pexpect.spawn(
                "ssh",
                [self._sshHost, "cd " + self._pathToDir + "; ./" + self._pathToTool, command, data]
            )
            process.expect("oe@rzssh1.informatik.uni-hamburg.de's password:")
            time.sleep(0.1)
            process.sendline(self._sshInput.readline())
            time.sleep(2)
            process.expect(pexpect.EOF)
            return True
        except CalledProcessError as cpe:
            self._errorObject = cpe
            return False
