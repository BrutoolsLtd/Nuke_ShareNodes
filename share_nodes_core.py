# share_nodes_core.py
# Author: Esteban Ortega
# Date: 03/11/21

"""ShareNodes core functionality , which includes send and received
scripts, this is the module used to launch the ShareNodes tool from
within Nuke."""

import sys
import getpass
import uuid
import pymongo
import datetime

import nuke

from PySide.QtGui import *
from share_nodes_ui import ShareNodesUI

# Here we will define some constants
CLIENT = pymongo.MongoClient("mongodb://localhost:27017/")
DB = CLIENT['ShareNodesDB']
USER_COLLECTION = DB['users']
CLIPBOARD_COLLECTION = DB['clipboards']
SCRIPT_LOCATION = 'F:/clipboards'
CURRENT_USER = getpass.getuser()


class ShareNodesCore(ShareNodesUI):

    def __init__(self):
        super(ShareNodesCore, self).__init__()

        self.all_users = [user for user in USER_COLLECTION.find()]
        self.populate_user_list_widget()

        ########################################################################
        # Connect signals
        ########################################################################
        self.search_users_QLineEdit.textChanged.connect(self.populate_user_list_widget)
        self.send_QPushButton.clicked.connect(self.on_send_clipboard)
        self.history_close_QPushButton.clicked.connect(self.close)
        self.paste_QPushButton.clicked.connect(self.paste_clipboard)
        self.history_tableWidget.currentCellChanged.connect(self.on_selection_change)

        ########################################################################
        # Execute some methods at start up of app.
        ########################################################################
        self.populate_history_widget()

    def on_selection_change(self, index):
        """Executes when selection is changed in history_tableWidget.
        Args:
            index: Current selection index return by cell changed in
            history_tableWidget.
        """

        item = self.history_tableWidget.item(index, 0)
        sender_item = item.data(32)
        note = sender_item['note']
        self.received_notes_QPlainTextEdit.setPlainText(note)

        return

    def paste_clipboard(self):
        """Get sent script and paste script into Nuke."""

        row = self.history_tableWidget.currentRow()
        item = self.history_tableWidget.item(row, 0)
        sender_item = item.data(32)
        script = sender_item['nuke_file']

        nuke.nodePaste('{}/{}'.format(SCRIPT_LOCATION, script))

        return

    def on_send_clipboard(self):
        """Executes when send button is pushed."""

        row_count = self.stack_QListWidget.count()

        if not row_count:
            QMessageBox.information(self, 'Warning', 'No user selected')

            return

        send_time = datetime.datetime.now()
        script = '{}.nk'.format(str(uuid.uuid1()))
        nuke.nodeCopy('{}/{}'.format(SCRIPT_LOCATION, script))

        for index in range(row_count):
            user_object = self.stack_QListWidget.item(index).data(32)
            doc = dict()
            doc['sender'] = CURRENT_USER
            doc['submitted_at'] = send_time
            doc['destination_user'] = user_object['login']
            doc['nuke_file'] = script
            doc['note'] = self.text_note_QPlainTextEdit.toPlainText()
            CLIPBOARD_COLLECTION.save(doc)

        self.close()

    def populate_history_widget(self):
        """Populates history_tableWidget with name and date."""
        query = CLIPBOARD_COLLECTION.find({'destination_user': CURRENT_USER}).sort('submitted_at', -1)
        self.history_tableWidget.setRowCount(query.count())
        for index, destination_user in enumerate(query):
            sender_query = USER_COLLECTION.find_one({'login': destination_user['sender']})
            item1 = QTableWidgetItem(sender_query['name'])
            item1.setData(32, destination_user)
            item2 = QTableWidgetItem(self.get_time_difference(destination_user['submitted_at']))
            self.history_tableWidget.setItem(index, 0, item1)
            self.history_tableWidget.setItem(index, 1, item2)

        return

    @staticmethod
    def get_time_difference(date):
        """Calculates time difference since script was sent.
        Args:
            date: datetime object representing the date when script was sent.

        returns:
            An string specifying the amount of time (seconds, minutes or hrs)
            since script was sent.
        """

        delta = datetime.datetime.today() - date
        if delta.days:
            return '{} day(s)'.format(delta.days)

        seconds = delta.seconds
        if seconds < 60:
            return "A few seconds ago"
        elif seconds < 3600:
            return '{} minute(s) ago'.format(seconds/60)
        elif seconds < 86400:
            return '{} hour(s) ago'.format(seconds/3600)

    def populate_user_list_widget(self):
        """Add user names and data (dictionary) for each user in
        list_users_QListWidget.
        """

        self.list_users_QListWidget.clear()
        search_pattern = self.search_users_QLineEdit.text().lower()

        for user in self.all_users:
            name = user['name']

            if search_pattern in name.lower():
                item = QListWidgetItem(name)
                item.setData(32, user)
                item.setToolTip(self.create_user_tooltip(user))
                self.list_users_QListWidget.addItem(item)
        self.list_users_QListWidget.sortItems()

        return

    @staticmethod
    def create_user_tooltip(user):
        """Creates a user tooltip string wot show on widget

        Args:
            user:Dictionary with user information.
        Returns:
            Formatted string for tooltip.
        """

        return 'Email: {}\nLogin: {}\nAge: {}'.format(user['email'],
                                                      user['login'],
                                                      user['age'])


def launch_share_nodes():
    """Creates an Qt application to launch share nodes tool.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    win = ShareNodesCore()
    win.show()
    app.exec_()
