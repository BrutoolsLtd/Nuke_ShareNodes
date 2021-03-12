# share_nodes_ui.py
# Author: Esteban Ortega
# Date: 03/11/21

"""ShareNodes UI , the view part of the tool."""

from PySide.QtGui import *
from PySide.QtCore import *


class ShareNodesUI(QTabWidget):
    """Class which represent the main window for sharing nodes.
    """

    def __init__(self):

        super(ShareNodesUI, self).__init__()

        self.setWindowTitle('Share Nodes / Script')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.resize(500, 600)
        self.setMinimumSize(500, 600)

        ########################################################################
        # Create Widgets
        ########################################################################

        # Create Widgets for Send Tab
        ########################################################################
        users_QLabel = QLabel('Users')
        self.list_users_QListWidget = QListWidget()
        self.list_users_QListWidget.setDragEnabled(True)

        search_QLabel = QLabel('Search')
        self.search_users_QLineEdit = QLineEdit()

        stack_label = QLabel('Sent To')
        self.stack_QListWidget = QListWidget()
        self.stack_QListWidget.setAcceptDrops(True)

        note_label = QLabel('Note / Message')

        self.text_note_QPlainTextEdit = QPlainTextEdit()

        self.send_QPushButton = QPushButton('Send')
        self.send_close_QPushButton = QPushButton('Close')

        # Create Widgets for History Tab
        ########################################################################
        history_label = QLabel('History')
        self.history_tableWidget = HistoryTableWidget()

        notes_label = QLabel('Notes')
        self.received_notes_QPlainTextEdit = QPlainTextEdit()

        self.paste_QPushButton = QPushButton('Paste')
        self.paste_QPushButton.setShortcut('Space')
        self.history_close_QPushButton = QPushButton('Close')

        # Create main widgets for Send and History tabs
        ########################################################################
        self.send_main_widget = QWidget()
        self.history_main_widget = QWidget()

        ########################################################################
        # Create Layouts and add widgets
        ########################################################################

        # Create Layout for Send tab
        ########################################################################
        send_layout = QHBoxLayout()

        send_layout_left = QVBoxLayout()
        send_layout_left.addWidget(users_QLabel)

        search_layout = QHBoxLayout()
        search_layout.addWidget(search_QLabel)
        search_layout.addWidget(self.search_users_QLineEdit)

        send_layout_left.addLayout(search_layout)

        send_layout_left.addWidget(self.list_users_QListWidget)

        send_layout_right = QVBoxLayout()
        send_layout_right.addWidget(stack_label)
        send_layout_right.addWidget(self.stack_QListWidget)
        send_layout_right.addWidget(note_label)
        send_layout_right.addWidget(self.text_note_QPlainTextEdit)

        send_action_layout = QHBoxLayout()
        send_action_layout.addWidget(self.send_QPushButton)
        send_action_layout.addWidget(self.send_close_QPushButton)

        send_layout_right.addLayout(send_action_layout)

        send_layout.addLayout(send_layout_left)
        send_layout.addLayout(send_layout_right)

        # Create Layout for History tab
        ########################################################################
        history_layout = QHBoxLayout()

        history_layout_left = QVBoxLayout()
        history_layout_left.addWidget(history_label)
        history_layout_left.addWidget(self.history_tableWidget)

        history_action_layout = QHBoxLayout()
        history_action_layout.addWidget(self.paste_QPushButton)
        history_action_layout.addWidget(self.history_close_QPushButton)

        history_layout_left.addLayout(history_action_layout)

        history_layout_right = QVBoxLayout()
        history_layout_right.addWidget(notes_label)
        history_layout_right.addWidget(self.received_notes_QPlainTextEdit)

        history_layout.addLayout(history_layout_left)
        history_layout.addLayout(history_layout_right)

        # Set layout for main widgets
        ########################################################################
        self.send_main_widget.setLayout(send_layout)
        self.history_main_widget.setLayout(history_layout)

        # Add tabs to Tabwidget (Main UI)
        ########################################################################
        self.addTab(self.send_main_widget, 'Send')
        self.addTab(self.history_main_widget, 'History')

        ########################################################################
        # Set Style sheets
        ########################################################################
        self.search_users_QLineEdit.setStyleSheet(self.get_style_sheet())

        ########################################################################
        # Connect signals
        ########################################################################
        self.send_close_QPushButton.clicked.connect(self.close)

    @staticmethod
    def get_style_sheet():
        """Styles the QLineEdit for searching users."""

        return '''padding: 2px 2px 2px 20px;
                  background-image: url(zoom.png);
                  background-position: left;
                  background-repeat: no-repeat'''


class HistoryTableWidget(QTableWidget):
    '''Defining / customizing some properties of QTableWidget, to be
       used in History tab.
    '''

    def __init__(self):
        super(HistoryTableWidget, self).__init__()

        self.setColumnCount(2)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setHorizontalHeaderItem(0, QTableWidgetItem('Name'))
        self.setHorizontalHeaderItem(1, QTableWidgetItem('Date'))
        self.horizontalHeader().setStretchLastSection(True)
        # self.horizontalHeader().setResizeMode()
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
