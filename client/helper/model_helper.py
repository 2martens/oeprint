from PyQt5.QtGui import QStandardItem

__author__ = "Tim Kilian"

def create_new_item(text):
    item = QStandardItem()
    item.setText(text)
    item.setCheckable(True)
    item.setEditable(False)
    return item