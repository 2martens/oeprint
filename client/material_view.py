from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QBoxLayout, QTreeView, QLabel, QFormLayout

from client.data import DataStorage, Material

__author__ = "Jim Martens"


class MaterialView(QWidget):
    """
    Displays the material view.
    """

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self._layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self._layout)
        # initialize tree view
        self._treeView = QTreeView()
        self._material_model = self._get_material_model()
        self._treeView.setModel(self._material_model)
        # initialize detail view
        self._detailView = QWidget()
        self._detailLayout = QBoxLayout(QBoxLayout.TopToBottom)
        self._detailView.setLayout(self._detailLayout)

        self._detailPanels = {}
        self._currentDetailPanel = None

        # add widgets to layout
        self._layout.addWidget(QLabel("List of Materials"))
        self._layout.addWidget(self._treeView)
        self._layout.addWidget(self._detailView)

        self._create_detail_view()
        # hide detail view on start
        self._detailView.hide()

        # add event listener for selection change
        self._treeView.clicked.connect(self._on_selection_change)

    @staticmethod
    def _get_material_model():
        data = DataStorage()
        materials = data.get_materials()
        model = QStandardItemModel()
        for name in materials:
            material = materials[name]
            item = QStandardItem()
            item.setText(name)
            item.setCheckable(True)
            item.setEditable(False)
            sub_materials = material.get_materials()
            for sub_material in sub_materials:
                sub_item = QStandardItem()
                sub_item.setText(sub_material.get_name())
                sub_item.setCheckable(True)
                sub_item.setEditable(False)
                item.appendRow(sub_item)

            model.appendRow(item)

        return model

    def _on_selection_change(self, model_index):
        """
        Called on selecting a new item in the treeView.
        :param model_index: index of selected item
        :type model_index: QModelIndex
        """
        data = DataStorage()
        materials = data.get_materials()
        selected_item = self._material_model.itemFromIndex(model_index)  # type: QStandardItem
        current_material_name = selected_item.text()
        parent_item = selected_item.parent()
        current_material = None

        if parent_item is not None:
            parent_item.setCheckState(2 if self._all_children_are_set(parent_item) else 0);

            parent_material = materials[parent_item.text()]
            sub_materials = parent_material.get_materials()
            for sub_material in sub_materials:
                if sub_material.get_name() == selected_item.text():
                    current_material = sub_material
                    break
        else:
            current_material = materials[current_material_name]

        self._check_all_children(selected_item)
        self._show_detail_view(current_material)

    def _check_all_children(self, parent_item):
        if parent_item.hasChildren():
            for row in range(parent_item.rowCount()):
                parent_item.child(row).setCheckState(parent_item.checkState());

    def _all_children_are_set(self, parent_item):
        if parent_item.hasChildren():
            for row in range(parent_item.rowCount()):
                if parent_item.child(row).checkState()==0:
                    return False
            return True
        return False

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
            # TODO transform list into range (if multiple pages)
            # layout.addRow("Page(s)", QLabel(material.get_pages()))

        self._detailView.show()
