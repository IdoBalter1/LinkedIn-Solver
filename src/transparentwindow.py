#!/usr/bin/env python3

# https://stackoverflow.com/questions/68594746/pyqt5-transparent-background-but-also-interactable

import sys
import ctypes
from ctypes import wintypes

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
import argparse
# from PIL import Image

# This overrides Qt's silly trapping of Ctrl-C,
# so you don't have to Ctrl-\ and get a core dump every time.
from PyQt5 import QtCore, QtGui, QtWidgets
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class TransWin(QMainWindow):

    def __init__(self, imgfile, position, opacity):
        super().__init__()

        self.imgfile = imgfile
        self.x0, self.y0 = position
        self.opacity = opacity/100

        self.drawing = False
        self.lastPoint = QPoint()

        self.initUI()

    def initUI(self):
        self.background = QPixmap(self.imgfile)
        width = self.background.width()
        height = self.background.height()
        self.setGeometry(self.x0, self.y0, width, height)

        # Translucent background
        self.setWindowOpacity(self.opacity)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set window flags for Windows - remove X11BypassWindowManagerHint
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |    # Always on top
            Qt.FramelessWindowHint |     # No title bar
            Qt.Tool                      # Tool window (doesn't show in taskbar)
        )
        
        # Prevent window from being minimized or hidden
        self.setAttribute(Qt.WA_ShowWithoutActivating, False)
        
        # Enable click-through using Windows API
        self.enable_click_through()

    def enable_click_through(self):
        """Enable click-through on Windows using Windows API"""
        try:
            # Wait a bit for window to be fully created
            QtWidgets.QApplication.processEvents()
            
            hwnd = int(self.winId())
            
            # Windows API constants
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x80000
            WS_EX_TRANSPARENT = 0x20
            WS_EX_NOACTIVATE = 0x8000000  # Prevent activation
            
            # Get current window style
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            
            # Add layered, transparent, and no-activate flags
            style = style | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_NOACTIVATE
            
            # Set the new style
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            
            # Force window to stay visible
            ctypes.windll.user32.ShowWindow(hwnd, 1)  # SW_SHOWNORMAL
        except Exception as e:
            print(f"Warning: Could not enable click-through: {e}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)
    
    def showEvent(self, event):
        """Ensure window stays visible when shown"""
        super().showEvent(event)
        self.enable_click_through()  # Re-apply click-through after show

    def keyPressEvent(self, e):
        print("keypress")
        if e.text() == 'q':
            QApplication.quit()




