from PyQt5.QtWidgets import QMessageBox

__author__ = "Jim Martens"


def show_error_alert(message):
    box = QMessageBox()
    box.setText("Error: " + message)
    box.exec()
