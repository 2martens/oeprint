import configparser
from shutil import copyfile

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QGridLayout, QLabel, QLineEdit


class Config:
    """Config accessor class"""
    def __init__(self, configfile='config.ini'):
        self.__configfile = configfile
        self.__config = self.__read()

    def get(self, section, key):
        """Returns a config value

        :param section: the section
        :type section: str
        :param key: the key
        :type key: str
        """
        return self.__config[section][key]

    def set(self, section, key, value):
        """Sets a config value

        :param section: the section
        :type section: str
        :param key: the key
        :type key: str
        :param value: the value
        :type value: str
        """
        self.__config[section][key] = value

    def write(self):
        """Writes the settings"""
        self.__write()

    def ___create_config_file(self):
        """Creates the config file"""
        config_file_template = 'config.ini.template'
        copyfile(config_file_template, self.__configfile)

    def __read(self):
        """Returns the config parser for the config file"""
        config = configparser.ConfigParser()
        try:
            with open(self.__configfile, 'r') as configfile:
                config.read_file(configfile)
        except FileNotFoundError:
            self.___create_config_file()
            with open(self.__configfile, 'r') as configfile:
                config.read_file(configfile)

        return config

    def __write(self):
        """Writes the config file for the given config"""
        with open(self.__configfile, 'w') as configfile:
            self.__config.write(configfile)


class ConfigDialog(QDialog):
    """Dialog class for configuration dialog"""
    def __init__(self, parent=None):
        """Initializes the dialog"""
        super(ConfigDialog, self).__init__(parent)
        self.__config = Config()

        # create form elements
        self.submitButton = QPushButton('&Save')
        ssh_host_label = QLabel('SSH-Host')
        self.sshHostLine = QLineEdit()
        self.sshHostLine.setText(self.__config.get('SSH', 'host'))

        # create form layout
        form_layout = QGridLayout()
        form_layout.addWidget(ssh_host_label, 0, 0)
        form_layout.addWidget(self.sshHostLine, 0, 1)

        # create main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.submitButton)
        # connect submit button with submit action
        self.submitButton.clicked.connect(self.__save)
        self.setLayout(main_layout)
        self.setWindowTitle('Preferences')

    def __save(self):
        """Saves the preferences"""
        ssh_host = self.sshHostLine.text()
        self.__config.set('SSH', 'host', ssh_host)
        self.__config.write()
        self.hide()
