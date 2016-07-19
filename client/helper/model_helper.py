from PyQt5 import QtCore

from PyQt5.QtGui import QStandardItem

__author__ = "Tim Kilian"


def create_new_item(text):
    item = QStandardItem()
    item.setText(text)
    item.setCheckable(True)
    item.setEditable(False)
    return item


def check_item(item):
    item.setCheckState(QtCore.Qt.Checked)
    check_all_children(item)
    check_parents(item)


def disable_item(item):
    item.setCheckState(QtCore.Qt.Unchecked)
    check_all_children(item)
    check_parents(item)


def reset_items(model):
    for row in range(model.rowCount()):
        disable_item(model.item(row))


def check_parents(item):
    if item.hasChildren() is False:
        item = item.parent()
    while item is not None:
        item.setCheckState(QtCore.Qt.Checked if all_children_are_set(item) else QtCore.Qt.Unchecked)
        item = item.parent()


def check_all_children(parent_item):
    if parent_item.hasChildren():
        for row in range(parent_item.rowCount()):
            child = parent_item.child(row)
            child.setCheckState(parent_item.checkState())
            check_all_children(child)


def all_children_are_set(parent_item):
    if parent_item.hasChildren():
        for row in range(parent_item.rowCount()):
            if parent_item.child(row).checkState()==0:
                return False
        return True
    return False


def is_checked(item):
    return item.checkState()==QtCore.Qt.Checked


def get_item(model, name):
    for row in range(model.rowCount()):
        item = _dfs(model.item(row), name)
        if item is not None:
            return item
    return None


def _dfs(root, name):
    if root.text() == name:
        return root
    if root.hasChildren():
        for row in range(root.rowCount()):
            result = _dfs(root.child(row), name)
            if result is not None:
                return result
    return None
