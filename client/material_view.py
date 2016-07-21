from PyQt5.QtWidgets import QWidget, QBoxLayout, QLabel, QFormLayout, QTreeWidget

from client.data import DataStorage, Material
from client.helper.model_helper import *
from client.print_view import PrintView

import itertools


__author__ = "Jim Martens"


class MaterialView(QWidget):
    """
    Displays the material view.
    """
    _material_model = None # type: QTreeWidget

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self._layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self._layout)
        # initialize tree view
        self._treeWidget = QTreeWidget()
        # self._treeWidget.setModel(self._get_material_model())
        self._treeWidget.setColumnCount(2)
        self._treeWidget.setHeaderLabels(["Material name", "Print amount"])
        self._initialize_model()
        # initialize detail view
        self._detailView = QWidget()
        self._detailLayout = QBoxLayout(QBoxLayout.TopToBottom)
        self._detailView.setLayout(self._detailLayout)
        # initialize print view
        self._print_view = PrintView()
        self._print_view.set_parent_model(self._treeWidget)

        self._detailPanels = {}
        self._currentDetailPanel = None

        # add widgets to layout
        self._layout.addWidget(QLabel("List of Materials"))
        self._layout.addWidget(self._treeWidget)
        self._layout.addWidget(self._detailView)
        self._layout.addWidget(self._print_view)

        self._resize_columns()

        self._create_detail_view()
        # hide detail view on start
        self._detailView.hide()

        # add event listener for selection change
        self._treeWidget.setEditTriggers(self._treeWidget.NoEditTriggers)
        self._treeWidget.itemDoubleClicked.connect(self._check_edit)
        self._treeWidget.selectionModel().currentChanged.connect(self._on_selection_change)
        self._treeWidget.clicked.connect(self._on_selection_change)
        self._treeWidget.expanded.connect(self._resize_columns)
        self._treeWidget.collapsed.connect(self._resize_columns)

    @staticmethod
    def get_model():
        return MaterialView._material_model

    @staticmethod
    def reset_check_state_and_print_amount():
        reset_items_tree(MaterialView._material_model)

    def _resize_columns(self):
        self._treeWidget.resizeColumnToContents(0)
        self._treeWidget.resizeColumnToContents(1)

    def _initialize_model(self):
        data = DataStorage()
        materials = data.get_materials()

        for name in materials:
            MaterialView._add_material(materials[name], self._treeWidget)

        if MaterialView._material_model is None:
            MaterialView._material_model = self._treeWidget

    @staticmethod
    def _add_material(material, item):
        sub_item = create_new_tree_item(material.get_name(), item)
        for sub_material in material.get_materials():
            MaterialView._add_material(sub_material, sub_item)

    def _check_edit(self, item, column):
        """
        Checks if the column of the item can be edited.
        :param item:
        :type item: QTreeWidgetItem
        :param column:
        :type column: number
        """
        if column == 1:
            self._treeWidget.editItem(item, column)

    def _on_selection_change(self, model_index):
        """
        Called on selecting a new item in the treeView.
        :param model_index: index of selected item
        :type model_index: QModelIndex
        """
        data = DataStorage()
        materials = data.get_materials()
        selected_item = self._treeWidget.itemFromIndex(model_index)  # type: QTreeWidgetItem
        current_material_name = selected_item.text(0)
        parent_item = selected_item.parent()
        current_material = None

        if parent_item is not None:
            check_parents_tree(parent_item)

            parent_material = data.get_material(parent_item.text(0))
            sub_materials = parent_material.get_materials()
            for sub_material in sub_materials:
                if sub_material.get_name() == selected_item.text(0):
                    current_material = sub_material
                    break
        else:
            current_material = materials[current_material_name]

        check_all_children_tree(selected_item)
        self._show_detail_view(current_material)

    def _create_detail_view(self):
        """
        Adds the permanent elements to the detail view.
        """
        self._detailLayout.addWidget(QLabel("Detail view for selected material"))

    def _show_detail_view(self, material: Material):
        """
        Shows the detail view for the selected material.
        :param material:
        :type material: Material
        """
        if self._currentDetailPanel is not None:
            self._currentDetailPanel.hide()
        if material.get_name() in self._detailPanels:
            self._currentDetailPanel = self._detailPanels[material.get_name()]
            self._currentDetailPanel.show()
        else:
            panel = QWidget()
            layout = QFormLayout()
            panel.setLayout(layout)

            # add panel to parent layout
            self._detailLayout.addWidget(panel)
            # save panel for future use
            self._detailPanels[material.get_name()] = panel
            self._currentDetailPanel = panel

            # panel
            layout.addRow("Filename", QLabel(material.get_filename()))
            pages = material.get_pages()
            if pages is not None:
                ranges = list(self._determine_ranges(pages))
                page_string = self._format_ranges(ranges)
                layout.addRow("Page(s)", QLabel(page_string))

        self._detailView.show()

    @staticmethod
    def _determine_ranges(source: list):
        """
        Determines the existing ranges in the list of pages.
        :param source:
        :type source: list
        """
        for a, b in itertools.groupby(enumerate(source), lambda x: x[1] - x[0]):
            b = list(b)
            yield b[0][1], b[-1][1]

    @staticmethod
    def _format_ranges(ranges: list):
        """
        Formats the list of ranges into a nice string.
        :param ranges:
        :type ranges: list
        :return: string
        """
        returnString = ""
        for lowerBound, upperBound in ranges:
            if returnString:
                returnString += ", "
            if (lowerBound == upperBound):
                returnString += str(lowerBound)
            else:
                returnString += str(lowerBound) + "-" + str(upperBound)

        return returnString
