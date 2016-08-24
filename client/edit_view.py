from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QWidget

from data import Configuration
from data import DataStorage
from helper.model_helper import create_new_tree_item, get_item, is_checked


class EditView(QDialog):
    """
    Displays the edit view
    """
    _material_model = None  # type: QTreeWidget
    _configuration_model = None  # type: QTreeWidget
    
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self._layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.setLayout(self._layout)
        self.setWindowTitle('Edit configuration')
        
        self._configurationTreeWidget = QTreeWidget()
        self._configurationTreeWidget.setColumnCount(2)
        self._configurationTreeWidget.setHeaderLabels(["Configuration name", "Print amount"])
        self._materialTreeWidget = QTreeWidget()
        self._materialTreeWidget.setColumnCount(2)
        self._materialTreeWidget.setHeaderLabels(["Material name", "Print amount"])
        self._initialize_material_model()
        
        self._currentConfiguration = None # type: Configuration
        
        config_widget = QWidget()
        self._configLayout = QBoxLayout(QBoxLayout.TopToBottom)
        self._nameField = QLineEdit()
        self._nameField.setEnabled(False)
        name_form_layout = QFormLayout()
        name_form_layout.addRow('Name:', self._nameField)
        self._configLayout.addLayout(name_form_layout)
        self._configLayout.addWidget(QLabel('List of configurations'))
        self._configLayout.addWidget(self._configurationTreeWidget)
        config_widget.setLayout(self._configLayout)
        
        self._saveButton = QPushButton("Save")
        material_widget = QWidget()
        self._materialLayout = QBoxLayout(QBoxLayout.TopToBottom)
        self._materialLayout.addWidget(self._saveButton)
        self._materialLayout.addWidget(QLabel('List of materials'))
        self._materialLayout.addWidget(self._materialTreeWidget)
        material_widget.setLayout(self._materialLayout)
        
        self._layout.addWidget(config_widget)
        self._layout.addWidget(material_widget)

        # add event listener for selection change
        self._configurationTreeWidget.setEditTriggers(self._configurationTreeWidget.NoEditTriggers)
        self._materialTreeWidget.setEditTriggers(self._materialTreeWidget.NoEditTriggers)
        self._configurationTreeWidget.itemDoubleClicked.connect(self._check_edit_configuration)
        self._materialTreeWidget.itemDoubleClicked.connect(self._check_edit_material)
        self._materialTreeWidget.expanded.connect(self._resize_columns)
        self._materialTreeWidget.collapsed.connect(self._resize_columns)
        self._saveButton.clicked.connect(self._save)

    @staticmethod
    def get_material_model():
        return EditView._material_model

    @staticmethod
    def get_configuration_model():
        return EditView._configuration_model
        
    def _resize_columns(self):
        self._materialTreeWidget.resizeColumnToContents(0)
        self._materialTreeWidget.resizeColumnToContents(1)
        self._configurationTreeWidget.resizeColumnToContents(0)
        self._configurationTreeWidget.resizeColumnToContents(1)
        
    def _check_edit_material(self, item, column):
        """
        Checks if the column of the item can be edited and set edit state if that is the case.
        :param item:
        :type item: QTreeWidgetItem
        :param column:
        :type column: number
        """
        if column == 1:
            self._materialTreeWidget.editItem(item, column)
            
    def _check_edit_configuration(self, item, column):
        """
        Checks if the column of the item can be edited and set edit state if that is the case.
        :param item:
        :type item: QTreeWidgetItem
        :param column:
        :type column: number
        """
        if column == 1:
            self._configurationTreeWidget.editItem(item, column)
        
    def _initialize_material_model(self):
        data = DataStorage()
        materials = data.get_materials()
        materials_order = data.get_materials_order()

        for name in materials_order:
            EditView._add_material(materials[name], self._materialTreeWidget)

        if EditView._material_model is None:
            EditView._material_model = self._materialTreeWidget

    @staticmethod
    def _add_material(material, item):
        sub_item = create_new_tree_item(material.get_name(), item)
        for sub_material in material.get_materials():
            EditView._add_material(sub_material, sub_item)
            
    def _initialize_configuration_model(self, configuration):
        data = DataStorage()
        configurations = data.get_configurations()
        configurations_order = data.get_configurations_order()

        for name in configurations_order:
            if name == configuration.get_name():
                continue
            EditView._add_configuration(configurations[name], self._configurationTreeWidget)

        EditView._configuration_model = self._configurationTreeWidget
        
        material_print_amounts = configuration.get_material_print_amounts()
        for material in configuration.get_materials():
            item = get_item(self._materialTreeWidget.invisibleRootItem(), material.get_name())
            if item is not None:
                print_amount = material_print_amounts[material.get_name()]
                item.setText(1, str(print_amount))

        configuration_print_amounts = configuration.get_config_print_amounts()
        for configuration in configuration.get_configurations():
            item = get_item(self._configurationTreeWidget.invisibleRootItem(), configuration.get_name())
            if item is not None:
                print_amount = configuration_print_amounts[configuration.get_name()]
                item.setText(1, str(print_amount))

    @staticmethod
    def _add_configuration(configuration, item):
        create_new_tree_item(configuration.get_name(), item)
    
    def _save(self):
        self.done(QDialog.Accepted)

    def show_for_configuration(self, configuration):
        """
        Shows the window for the given configuration.
        :param configuration:
        :type configuration: Configuration
        """
        self._currentConfiguration = configuration
        self._initialize_configuration_model(configuration)
        self._resize_columns()
        self._nameField.setText(configuration.get_name())
        self.exec()
