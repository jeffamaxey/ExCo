
# -*- coding: utf-8 -*-

"""
Copyright (c) 2018 Matic Kukovec. 
"""

import keyword
import builtins
import re
import functions
import data
import time
import lexers


class Text(data.QsciLexerCustom):
    """Lexer for styling normal text documents"""
    # Class variables
    styles = {
        "Default" : 0
    }
    
    def __init__(self, parent=None):
        """Overridden initialization"""
        #Initialize superclass
        super().__init__()
        #Set the font colors
        self.setFont(data.get_current_font(), 0)
        #Reset autoindentation style
        self.setAutoIndentStyle(0)
        #Set the theme
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        # Papers
        self.setPaper(
            data.QColor(theme.Paper.Python.Default), 
            self.styles["Default"]
        )
        # Fonts
        lexers.set_font(self, "Default", theme.Font.Python.Default)
    
    def language(self):
        return "Plain text"
    
    def description(self, style):
        return "Text" if style == 0 else ""
    
    def defaultStyle(self):
        return self.styles["Default"]
    
    def braceStyle(self):
        return self.styles["Default"]
    
    def defaultFont(self, style):
        return data.QFont(data.current_font_name, data.current_font_size)
    
    def styleText(self, start, end):
        self.startStyling(start)
        self.setStyling(end - start, 0)


