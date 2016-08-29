from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from data import Configuration, DataStorage


class AddConfigurationDialog(QDialog):
    def __init__(self, parent=None):
        super(AddConfigurationDialog, self).__init__(parent)
        self._layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self._layout)
        self.setWindowTitle('Add configuration')

        self._nameField = QLineEdit()
        name_form_layout = QFormLayout()
        name_form_layout.addRow('Name:', self._nameField)
        self._layout.addLayout(name_form_layout)
        self._layout.addWidget(QLabel("You won't be able to change this name later."))
        self._cancelButton = QPushButton("Cancel")
        self._saveButton = QPushButton("Create")
        button_layout = QBoxLayout(QBoxLayout.LeftToRight)
        button_layout.addWidget(self._cancelButton)
        button_layout.addWidget(self._saveButton)
        self._layout.addLayout(button_layout)
        
        self._configuration = None
        
        self._cancelButton.clicked.connect(self.reject)
        self._saveButton.clicked.connect(self._saved)
        
    def _saved(self):
        name = self._nameField.text()
        self._configuration = Configuration(name)
        data = DataStorage()
        data.add_configuration(self._configuration)
        data.persist()
        self.accept()
        
    def get_configuration(self):
        """
        Returns the created configuration if called after executing the dialog or None otherwise.
        :rtype: Configuration
        """
        return self._configuration
