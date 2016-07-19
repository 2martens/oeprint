from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QBoxLayout, QTreeView, QLabel, QFormLayout, QPushButton

from client.data import DataStorage, Material
from client.helper.model_helper import *

import itertools

__author__ = "Jim Martens"


class MaterialView(QWidget):
    """
    Displays the material view.
    """
    _material_model = None

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self._layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self._layout)
        # initialize tree view
        self._treeView = QTreeView()
        self._treeView.setModel(self._get_material_model())
        # initialize detail view
        self._detailView = QWidget()
        self._detailLayout = QBoxLayout(QBoxLayout.TopToBottom)
        self._detailView.setLayout(self._detailLayout)

        self._detailPanels = {}
        self._currentDetailPanel = None

        self._printButton = QPushButton("Print")

        # add widgets to layout
        self._layout.addWidget(QLabel("List of Materials"))
        self._layout.addWidget(self._treeView)
        self._layout.addWidget(self._detailView)
        self._layout.addWidget(self._printButton)

        self._create_detail_view()
        # hide detail view on start
        self._detailView.hide()

        # add event listener for selection change
        self._treeView.clicked.connect(self._on_selection_change)
        self._printButton.clicked.connect(self._on_printbutton_press)

    @staticmethod
    def _get_material_model():
        if MaterialView._material_model is None:
            data = DataStorage()
            materials = data.get_materials()
            model = QStandardItemModel()

            parent_item = model.invisibleRootItem()
            for name in materials:
                MaterialView._get_submaterial_model(materials[name], parent_item)

            MaterialView._material_model = model
        return MaterialView._material_model

    @staticmethod
    def _get_submaterial_model(material, item):
        sub_item = create_new_item(material.get_name())
        item.appendRow(sub_item)
        for sub_material in material.get_materials():
            MaterialView._get_submaterial_model(sub_material, sub_item)

    def _on_selection_change(self, model_index):
        """
        Called on selecting a new item in the treeView.
        :param model_index: index of selected item
        :type model_index: QModelIndex
        """
        data = DataStorage()
        materials = data.get_materials()
        selected_item = self._get_material_model().itemFromIndex(model_index)  # type: QStandardItem
        current_material_name = selected_item.text()
        parent_item = selected_item.parent()
        current_material = None

        if parent_item is not None:
            check_parents(parent_item)

            parent_material = data.get_material(parent_item.text())
            sub_materials = parent_material.get_materials()
            for sub_material in sub_materials:
                if sub_material.get_name() == selected_item.text():
                    current_material = sub_material
                    break
        else:
            current_material = materials[current_material_name]

        check_all_children(selected_item)
        self._show_detail_view(current_material)

    def _on_printbutton_press(self):
        reset_items(self._get_material_model())
        pass

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

            # TODO add counter to tree view

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
