from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem


class TreeWidgetItem(QTreeWidgetItem):
    def setData(self, column, role, value):
        """
        Sets the data for the item.
        :param column:
        :type column: int
        :param role:
        :type role: int
        :param value:
        """
        current_status = self.checkState(column)
        super(TreeWidgetItem, self).setData(column, role, value)

        if role == Qt.CheckStateRole:
            if current_status != value:
                tree_widget = self.treeWidget()  # type: TreeWidget
                index = tree_widget.indexFromItem(self, column)
                tree_widget.itemChecked.emit(index)


class TreeWidget(QTreeWidget):
    itemChecked = pyqtSignal(QModelIndex)
    
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)
        self.itemChecked.connect(self._handle_item_checked)
    
    def _handle_item_checked(self):
        pass
