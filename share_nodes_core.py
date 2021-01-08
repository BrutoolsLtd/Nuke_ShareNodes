import sys

from PySide.QtGui import *
from PySide.QtCore import *

from share_nodes_ui import ShareNodesUI


class ShareNodesCore(ShareNodesUI):

    def __init__(self):
        super(ShareNodesCore, self).__init__()


app = QApplication(sys.argv)
win = ShareNodesCore()
win.show()
app.exec_()
