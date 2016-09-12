from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLineEdit

__author__ = "Jim Martens"


class SSHInput:
    def __init__(self, parent):
        self._parent = parent

    def readline(self):
        text, ok = QInputDialog.getText(self._parent, "Enter SSH password", "Password", QLineEdit.Password)
        if ok:
            return str(text)
        else:
            return ''
