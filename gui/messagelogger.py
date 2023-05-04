
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2019 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sip
import os.path
import collections
import traceback
import ast
import inspect
import math
import functools
import textwrap
import difflib
import re
import time
import settings
import functions
import data
import components
import themes


"""
----------------------------------------------------------------------------
Object for showing log messages across all widgets, mostly for debug purposes
----------------------------------------------------------------------------
"""
class MessageLogger(data.QWidget):
    """Simple subclass for displaying log messages"""
    class MessageTextBox(data.QTextEdit): 
        def contextMenuEvent(self, event):
            event.accept()
    
    #Controls and variables of the log window  (class variables >> this means that these variables are shared accross instances of this class)
    displaybox  = None      #QTextEdit that will display log messages
    layout      = None      #The layout of the log window
    parent      = None
    
    def __init__(self, parent):
        """Initialization routine"""
        #Initialize superclass, from which the current class is inherited, THIS MUST BE DONE SO THAT THE SUPERCLASS EXECUTES ITS __init__ !!!!!!
        super().__init__()
        
        #Initialize the log window
        self.setWindowTitle("LOGGING WINDOW")
        self.resize(500, 300)
        self.setWindowFlags(data.Qt.WindowStaysOnTopHint)
        # Set default font
        self.setFont(data.get_current_font())
        
        #Initialize the display box
        self.displaybox = MessageLogger.MessageTextBox(self)
        self.displaybox.setReadOnly(True)
        #Make displaybox click/doubleclick event also fire the log window click/doubleclick method
        self.displaybox.mousePressEvent         = self._event_mousepress
        self.displaybox.mouseDoubleClickEvent   = self._event_mouse_doubleclick
        self.keyPressEvent                      = self._keypress
        
        #Initialize layout
        self.layout = data.QGridLayout()
        self.layout.addWidget(self.displaybox)
        self.setLayout(self.layout)
        
        self.append_message("Ex.Co. debug log window loaded")
        self.append_message("LOGGING Mode is enabled")
        self._parent = parent
        
        #Set the log window icon
        if os.path.isfile(data.application_icon) == True:
            self.setWindowIcon(data.QIcon(data.application_icon))
    
    def _event_mouse_doubleclick(self, mouse_event):
        """Rereferenced/overloaded displaybox doubleclick event"""
        self.clear_log()
    
    def _event_mousepress(self, mouse_event):
        """Rereferenced/overloaded displaybox click event"""
        # Reset the click&drag context menu action
        components.ActionFilter.clear_action()
    
    def _keypress(self, key_event):
        """Rereferenced/overloaded MessageLogger keypress event"""
        pressed_key = key_event.key()
        if pressed_key == data.Qt.Key_Escape:
            self.close()
    
    def clear_log(self):
        """Clear all messages from the log display"""
        self.displaybox.clear()
        
    def append_message(self, *args, **kwargs):
        """Adds a message as a string to the log display if logging mode is enabled"""
        message = " ".join(args) if len(args) > 1 else args[0]
        #Check if message is a string class, if not then make it a string
        if not isinstance(message, str):
            message = str(message)
        #Check if logging mode is enabled
        if data.logging_mode == True:
            self.displaybox.append(message)
        #Bring cursor to the current message (this is in a QTextEdit not QScintilla)
        cursor = self.displaybox.textCursor()
        cursor.movePosition(data.QTextCursor.End)
        cursor.movePosition(data.QTextCursor.StartOfLine)
        self.displaybox.setTextCursor(cursor)



