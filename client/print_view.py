from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QComboBox, QLabel, QFormLayout
from PyQt5.QtWidgets import QWidget, QBoxLayout, QPushButton

from client.config import Config
from helper.model_helper import *

__author__ = "Jim Martens"


class PrintView(QWidget):
    """
    Displays the print view.
    """
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self._layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self._layout)
        # initialize
        config = Config()
        self._printerSelection = QComboBox()
        self._printerSelection.addItems(config.get("Data", "printers").split(","))
        self._printerSelection.setEditable(True)
        self._printButton = QPushButton("Print")

        form_layout = QFormLayout()
        form_layout.addRow("Printer:", self._printerSelection)
        self._layout.addLayout(form_layout)
        self._layout.addWidget(self._printButton)
        self._model = None # type: QTreeWidget

        # initialize event listener
        self._printButton.clicked.connect(self._print)

    def set_parent_model(self, model):
        self._model = model

    def _print(self):
        """
        Prints the selected materials.
        """
        print_amounts = self._calculate_print_amounts(self._model.invisibleRootItem())
        printer = self._printerSelection.currentText()
        # TODO implement synching with server

    def _calculate_print_amounts(self, root_item):
        """
        :param root_item:
        :type root_item: QTreeWidgetItem
        :rtype: dict
        """
        print_amounts = {}
        if root_item.childCount() > 0:
            for child_index in range(root_item.childCount()):
                child = root_item.child(child_index)
                if is_checked(child):
                    print_amounts[child.text(0)] = int(child.text(1))
                else:
                    child_print_amounts = self._calculate_print_amounts(child)
                    print_amounts.update(child_print_amounts)

        elif is_checked(root_item):
            print_amounts[root_item.text(0)] = int(root_item.text(1))

        return print_amounts
