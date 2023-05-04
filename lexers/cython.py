
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


class Cython(data.QsciLexerPython):
    """Cython - basically Python with added keywords"""
    #Class variables
    _kwrds = None
    styles = {
        "Default" : 0,
        "Comment" : 1,
        "Number" : 2,
        "DoubleQuotedString" : 3,
        "SingleQuotedString" : 4,
        "Keyword" : 5,
        "TripleSingleQuotedString" : 6,
        "TripleDoubleQuotedString" : 7,
        "ClassName" : 8,
        "FunctionMethodName" : 9,
        "Operator" : 10,
        "Identifier" : 11,
        "CommentBlock" : 12,
        "UnclosedString" : 13,
        "HighlightedIdentifier" : 14,
        "Decorator" : 15
    }
    _c_kwrds = [
        "void", "char", "int", "long", "short", "double", "float", 
        "const", "unsigned", "inline"
    ]
    _cython_kwrds = [
        "by", "cdef", "cimport", "cpdef", "ctypedef", "enum", "except?", 
        "extern", "gil", "include", "nogil", "property", "public", 
        "readonly", "struct", "union", "DEF", "IF", "ELIF", "ELSE"
    ]
    
    
    def __init__(self,  parent=None):
        """Overridden initialization"""
        #Initialize superclass
        super().__init__()
        #Initialize list with keywords
        #Initialize list with keywords
        built_ins = keyword.kwlist
        for i in builtins.__dict__.keys():
            if i not in built_ins:
                built_ins.append(i)
        self._kwrds = list(set(built_ins))
        #Transform list into a single string with spaces between list items
        #Add the C keywords supported by Cython
        self._kwrds.extend(self._c_kwrds)
        #Add the Cython keywords
        self._kwrds.extend(self._cython_kwrds)
        #Transform list into a single string with spaces between list items
        self._kwrds.sort()
        self._kwrds = " ".join(self._kwrds)
        #Reset autoindentation style
        self.setAutoIndentStyle(0)
        #Set the theme
        self.set_theme(data.theme)
    
    def set_theme(self, theme):
        for style in self.styles:
            # Papers
            self.setPaper(
                data.QColor(theme.Paper.Python.Default), 
                self.styles[style]
            )
            # Fonts
            lexers.set_font(self, style, getattr(theme.Font.Python, style))
    
    def keywords(self, state):
        """
        Overridden method for determining keywords,
        read the QScintilla QsciLexer class documentation on the Riverbank website.
        """
        return self._kwrds if state == 1 else None