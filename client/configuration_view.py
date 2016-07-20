from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QListView, QWidget, QBoxLayout, QSpinBox, QFormLayout, QPushButton, QLabel

from client.data import DataStorage, Configuration
from client.helper.model_helper import *
from client.material_view import MaterialView

__author__ = "Jim Martens"


class ConfigurationView(QWidget):
    """
    Displays the configuration view.
    """

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self._layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self._layout)
        # initialize list view
        self._listView = QListView()
        self._configuration_model = self._get_config_model()
        self._listView.setModel(self._configuration_model)
        # initialize detail view
        self._detailView = QWidget()
        self._detailLayout = QBoxLayout(QBoxLayout.TopToBottom)
        self._detailView.setLayout(self._detailLayout)

        self._detailPanels = {}
        self._currentDetailPanel = None

        # add widgets to layout
        self._layout.addWidget(QLabel("List of Configurations"))
        self._layout.addWidget(self._listView)
        self._layout.addWidget(self._detailView)

        self._create_detail_view()
        # hide detail view on start
        self._detailView.hide()

        # selected configs map
        self._selected_configs = {}
        self._selected_counter = 0

        # add event listener for selection change
        self._listView.clicked.connect(self._on_selection_change)
        self._listView.selectionModel().currentChanged.connect(self._on_selection_change)

    @staticmethod
    def _get_config_model():
        data = DataStorage()
        configurations = data.get_configurations()
        model = QStandardItemModel()

        for name in configurations:
            item = create_new_list_item(name)
            model.appendRow(item)

        return model

    def _on_selection_change(self, model_index):
        """
        Called on selecting a new item in the listView.
        :param model_index: index of selected item
        :type model_index: QModelIndex
        """
        data = DataStorage()
        configurations = data.get_configurations()
        selected_item = self._configuration_model.itemFromIndex(model_index) # type: QStandardItem
        current_config_name = selected_item.text()
        current_config = configurations[current_config_name] # type: Configuration
        self._show_detail_view(current_config)
        material_print_amounts = current_config.get_effective_material_print_amounts()

        if self._selected_counter == 0:
            MaterialView.reset_check_state_and_print_amount()

        for material in current_config.get_materials():
            item = get_item(MaterialView.get_model().invisibleRootItem(), material.get_name())
            if item is not None:
                print_amount = material_print_amounts[material.get_name()]
                if is_checked_list(selected_item):
                    check_item(item)
                    if current_config_name not in self._selected_configs:
                        print_amount += int(item.text(1))
                    else:
                        print_amount = int(item.text(1))

                item.setText(1, str(print_amount))

        if is_checked_list(selected_item) and current_config_name not in self._selected_configs:
            self._selected_configs[current_config_name] = True
            self._selected_counter += 1
        if not is_checked_list(selected_item) and current_config_name in self._selected_configs:
            self._selected_configs.pop(current_config_name)
            self._selected_counter -= 1

    def _create_detail_view(self):
        """
        Adds the permanent elements to the detail view.
        """
        edit_button = QPushButton("Edit")
        self._detailLayout.addWidget(QLabel("Detail view for selected configuration"))
        self._detailLayout.addWidget(edit_button)

    def _show_detail_view(self, configuration: Configuration):
        """
        Shows the detail view for the selected configuration.
        :param configuration:
        :type configuration: Configuration
        """
        if self._currentDetailPanel is not None:
            self._currentDetailPanel.hide()
        if configuration.get_name() in self._detailPanels:
            self._currentDetailPanel = self._detailPanels[configuration.get_name()]
            self._currentDetailPanel.show()
        else:
            panel = QWidget()
            layout = QFormLayout()
            panel.setLayout(layout)

            config_wide_counter = QSpinBox()
            config_wide_counter.setMinimum(1)
            config_wide_counter.setValue(1)

            # add panel to parent layout
            self._detailLayout.addWidget(panel)
            # save panel for future use
            self._detailPanels[configuration.get_name()] = panel
            self._currentDetailPanel = panel

            # panel
            layout.addRow("Print this config x times", config_wide_counter)
            layout.addRow("Child configurations", QLabel())
            configurations = configuration.get_configurations()
            config_print_amounts = configuration.get_config_print_amounts()
            for config in configurations: # type: Configuration
                config_counter = QSpinBox()
                config_counter.setMinimum(1)
                config_counter.setValue(config_print_amounts[config.get_name()])
                layout.addRow("Print config " + config.get_name() + " x times", config_counter)

        self._detailView.show()
