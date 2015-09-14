# -*- coding: utf-8 -*-
# imports for PyInstaller hook
import sys
import os

# PyInstaller hook for detecting run mode
def resource_path(relative_path):
     try:
         basedir = sys._MEIPASS
     except Exception:
         # we are running in a normal Python environment
         basedir = os.path.dirname(os.path.abspath(__file__))
     return os.path.join(basedir, relative_path)



