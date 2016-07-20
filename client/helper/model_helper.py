from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem

from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QTreeWidget

__author__ = "Tim Kilian"


def create_new_list_item(text):
    item = QStandardItem()
    item.setText(text)
    item.setCheckable(True)
    item.setEditable(False)
    return item


def create_new_tree_item(text, parent):
    item = QTreeWidgetItem(parent)
    item.setText(0, text)
    item.setText(1, str(0))
    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
    item.setCheckState(0, Qt.Unchecked)
    return item


# only for QStandardItems
def check_parents_list(item):
    """
    :param item:
    :type item: QStandardItem
    """
    if not item.hasChildren():
        item = item.parent()
    while item is not None:
        item.setCheckState(QtCore.Qt.Checked if all_children_are_set_list(item) else QtCore.Qt.Unchecked)
        item = item.parent()


def check_all_children_list(parent_item):
    """
    :param parent_item:
    :type parent_item: QStandardItem
    """
    if parent_item.hasChildren():
        for child_index in range(parent_item.rowCount()):
            child = parent_item.child(child_index)
            child.setCheckState(0, parent_item.checkState(0))
            check_all_children_list(child)


def all_children_are_set_list(parent_item):
    """
    :param parent_item:
    :type parent_item: QStandardItem
    """
    if parent_item.hasChildren():
        for row in range(parent_item.rowCount()):
            if parent_item.child(row).checkState() == Qt.Unchecked:
                return False
        return True
    return False


def is_checked_list(item):
    return item.checkState() == QtCore.Qt.Checked


def disable_item(item):
    item.setCheckState(QtCore.Qt.Unchecked)
    check_all_children_list(item)
    check_parents_list(item)

# end only for QStandarditems


def reset_items(model):
    for row in range(model.rowCount()):
        disable_item(model.item(row))


# only for QWidgetTreeItems
def check_item(item):
    """
    Checks an item.
    :param item:
    :type item: QTreeWidgetItem
    """
    item.setCheckState(0, QtCore.Qt.Checked)
    check_all_children_tree(item)
    check_parents_tree(item)


def reset_item_tree(item):
    """
    Resets an item.
    :param item:
    :type item: QTreeWidgetItem
    """
    item.setCheckState(0, Qt.Unchecked)
    item.setText(1, str(0))
    check_all_children_tree(item)
    check_parents_tree(item)


def reset_items_tree(model):
    """
    Resets all items.
    :param model:
    :type model: QTreeWidget
    """
    root_item = model.invisibleRootItem()
    for child_index in range(root_item.childCount()):
        reset_item_tree(root_item.child(child_index))


def check_parents_tree(item):
    if item.childCount() == 0:
        item = item.parent()
    while item is not None:
        item.setCheckState(0, QtCore.Qt.Checked if all_children_are_set_tree(item) else QtCore.Qt.Unchecked)
        item = item.parent()


def check_all_children_tree(parent_item):
    if parent_item.childCount() > 0:
        for child_index in range(parent_item.childCount()):
            child = parent_item.child(child_index)
            child.setCheckState(0, parent_item.checkState(0))
            check_all_children_tree(child)


def all_children_are_set_tree(parent_item):
    if parent_item.childCount() > 0:
        for row in range(parent_item.childCount()):
            if parent_item.child(row).checkState(0) == Qt.Unchecked:
                return False
        return True
    return False


def is_checked_tree(item):
    return item.checkState(0) == QtCore.Qt.Checked


def get_item(root_item, name):
    """
    Returns the item with given name in tree starting from root_item.
    :param root_item:
    :type root_item: QTreeWidgetItem
    :param name:
    :type name: str
    :rtype QTreeWidgetItem
    """
    for row in range(root_item.childCount()):
        item = _dfs(root_item.child(row), name)
        if item is not None:
            return item
    return None


def _dfs(root, name):
    """
    Searches the item with given name in tree starting from root.
    :param root:
    :type root: QTreeWidgetItem
    :param name:
    :type name: str
    :rtype: QTreeWidgetItem
    """
    if root.text(0) == name:
        return root
    if root.childCount() > 0:
        for row in range(root.childCount()):
            result = _dfs(root.child(row), name)
            if result is not None:
                return result
    return None

# end only for QWidgetTreeItems
