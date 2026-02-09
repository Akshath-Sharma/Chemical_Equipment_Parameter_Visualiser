from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


def update_history_ui(list_widget, history_data):
    list_widget.clear()
    for item in history_data[:5]:
        list_item = QListWidgetItem(f"📄 {item['filename']}\n{item['upload_date'][:10]}")
        list_item.setData(Qt.UserRole, item['id'])
        list_widget.addItem(list_item)