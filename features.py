"""
This file contains the features that helps for QA testing.
"""
from utilities import Errors, Commands, Checks


class Screenshot:

    def __init__(self):
        self.err = Errors()
        self.cmd = Commands()
        self.chk = Checks()

    def takeScreenshot(self):
        pass


class Screenrecord:
    pass
