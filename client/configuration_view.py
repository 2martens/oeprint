from PyQt5.QtCore import QModelIndex, QRect, QItemSelectionModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QListView, QWidget, QBoxLayout, QSpinBox, QFormLayout, QPushButton, QLabel

from data import DataStorage, Configuration
from edit_view import EditView
from helper.model_helper import *
from material_view import MaterialView

__author__ = "Jim Martens"


class ConfigurationView(QWidget):
    """
    Displays the configuration view.
    """

    def __init__(self, parent=None):
        super(ConfigurationView, self).__init__(parent)
        self._layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self._layout)
        self._editView = EditView(parent)
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
        self._currentConfiguration = None # type: Configuration
        self._config_wide_print_amounts = {}
        self._recalculateEffectivePrintAmounts = False

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

    def add_configuration(self, configuration):
        """
        Adds the given configuration to the list view and opens the edit view.
        :param configuration:
        :type configuration: Configuration
        """
        item = create_new_list_item(configuration.get_name())
        self._configuration_model.appendRow(item)
        self._editView.show_for_configuration(configuration)

    def select_first_item(self):
        rect = QRect(0,0,1,1)
        self._listView.setSelection(rect, QItemSelectionModel.Select)

    @staticmethod
    def _get_config_model():
        data = DataStorage()
        configurations_order = data.get_configurations_order()
        model = QStandardItemModel()

        for name in configurations_order:
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
        config_wide_print_amount = self._config_wide_print_amounts[current_config_name]
        material_print_amounts = current_config.get_effective_material_print_amounts(
            config_wide_print_amount,
            self._recalculateEffectivePrintAmounts
        )
        self._recalculateEffectivePrintAmounts = False

        if self._selected_counter == 0:
            MaterialView.reset_check_state_and_print_amount()

        for material in current_config.get_materials():
            item = get_item(MaterialView.get_model().invisibleRootItem(), material.get_name())
            if item is not None:
                print_amount = material_print_amounts[material.get_name()]
                if is_checked(selected_item):
                    check_item(item)
                    if current_config_name not in self._selected_configs:
                        print_amount += int(item.text(1))
                    else:
                        print_amount = int(item.text(1))

                item.setText(1, str(print_amount))

        if is_checked(selected_item) and current_config_name not in self._selected_configs:
            self._selected_configs[current_config_name] = True
            self._selected_counter += 1
        if not is_checked(selected_item) and current_config_name in self._selected_configs:
            self._selected_configs.pop(current_config_name)
            self._selected_counter -= 1

        self._currentConfiguration = current_config

    def _create_detail_view(self):
        """
        Adds the permanent elements to the detail view.
        """
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self._show_edit_view)
        self._detailLayout.addWidget(QLabel("Detail view for selected configuration"))
        self._detailLayout.addWidget(edit_button)

    def _change_config_wide_print_amount(self, new_value):
        self._config_wide_print_amounts[self._currentConfiguration.get_name()] = new_value
        self._recalculateEffectivePrintAmounts = True

    def _create_update_function_for_sub_configs(self, sub_config, configuration):
        def update_func(new_value):
            if self._currentConfiguration.get_name() == configuration.get_name():
                self._currentConfiguration.set_config_print_amount(sub_config, new_value)
            self._recalculateEffectivePrintAmounts = True
        return update_func
    
    def _show_edit_view(self):
        """
        Shows the edit view for the selected configuration.
        """
        self._editView.show_for_configuration(self._currentConfiguration)
        selected_indexes = self._listView.selectedIndexes()
        self._on_selection_change(selected_indexes[0])

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
            config_wide_counter.valueChanged.connect(self._change_config_wide_print_amount)

            # add panel to parent layout
            self._detailLayout.addWidget(panel)
            # save panel for future use
            self._detailPanels[configuration.get_name()] = panel
            self._currentDetailPanel = panel
            self._config_wide_print_amounts[configuration.get_name()] = 1

            # panel
            layout.addRow("Print this config x times", config_wide_counter)
            layout.addRow("Child configurations", QLabel())
            configurations = configuration.get_configurations()
            config_print_amounts = configuration.get_config_print_amounts()
            for config in configurations: # type: Configuration
                config_counter = QSpinBox()
                config_counter.setMinimum(1)
                config_counter.setValue(config_print_amounts[config.get_name()])
                update_func = self._create_update_function_for_sub_configs(config, configuration)
                config_counter.valueChanged.connect(update_func)
                layout.addRow("Print config " + config.get_name() + " x times", config_counter)

        self._detailView.show()
