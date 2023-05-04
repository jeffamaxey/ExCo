
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2021 Matic Kukovec. 
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
from .custombuttons import CustomButton


"""
---------------------------------------------------------
Custom context menu for the editors and REPL
---------------------------------------------------------
""" 
class ContextMenu(data.QGroupBox):
    class ContextButton(CustomButton):
        """
        Subclassed custom button
        """
        # The button's number in the context menu
        number = None
        
        def _fill_background_color(self):
            self.setAutoFillBackground(True)
            p = self.palette()
            p.setColor(
                self.backgroundRole(), 
                data.theme.Context_Menu_Background
            )
            self.setPalette(p)
        
        def _set_opacity(self, input_opacity):
            super()._set_opacity(input_opacity)
            self._fill_background_color()
        
        def _set_opacity_with_hex_edge(self, input_opacity):
            super()._set_opacity_with_hex_edge(input_opacity)
            self._fill_background_color()
        
        def mousePressEvent(self, event):
            """Overloaded widget click event"""
            button = event.button()
            if button == data.Qt.LeftButton and self.function != None:
                if components.ActionFilter.click_drag_action is None:
                    try:
                        # Execute the buttons stored function
                        self.function()
                    except:
                        traceback.print_exc()
                        message = "You need to focus one of the editor windows first!"
                        self.main_form.display.repl_display_message(
                            message, 
                            message_type=data.MessageType.ERROR
                        )
                else:
                    function_name = components.ActionFilter.click_drag_action.function.__name__
#                        print(self.number, function_name)
                    if self._parent.functions_type == "horizontal":
                        ContextMenu.horizontal_buttons[self.number] = function_name
                    elif self._parent.functions_type == "special":
                        ContextMenu.special_buttons[self.number] = function_name
                    elif self._parent.functions_type in ["standard", "plain"]:
                        ContextMenu.standard_buttons[self.number] = function_name
                        # Show the newly added function
                    message = f"Added function '{components.ActionFilter.click_drag_action.text()}' at button number {self.number}"
                    self.main_form.display.repl_display_message(
                        message, 
                        message_type=data.MessageType.SUCCESS
                    )
                    # Reset cursor and stored action
                    data.application.restoreOverrideCursor()
                    components.ActionFilter.click_drag_action = None
                # Close the function wheel
                self._parent.hide()
                event.accept()
            elif button == data.Qt.LeftButton or button != data.Qt.RightButton:
                event.ignore()
            else:
                # Close the function wheel
                self._parent.hide()
                event.accept()
        
        def dim(self, clear_hex_edge=False):
            """Set the buttons opacity to low and clear the function text"""
            # Set the opacity to low
            if clear_hex_edge == True:
                self._set_opacity(self.OPACITY_LOW)
            else:
                self._set_opacity_with_hex_edge(self.OPACITY_LOW)
        
        def highlight(self):
            """Set the buttons opacity to high and display the buttons function text"""
            # Set the opacity to full
            self._set_opacity_with_hex_edge(self.OPACITY_HIGH)
            # Display the stored function text
            self.main_form.display.write_to_statusbar(self.function_text)
    
    # Various references
    main_form = None
    # Painting offset
    offset = (0, 0)
    # Stored menu button
    button_list = None
    # Functions dictionary
    function_list = {}
    # Inner button positions, clockwise from the top, 
    # last position is in the middle
    inner_button_positions = [
        (-27, -24, 0),
        (14, 0, 1),
        (14, 48, 2),
        (-27, 72, 3),
        (-68, 48, 4),
        (-68, 0, 5),
        (-27, 24, 6)
    ]
    outer_button_positions = [
        (-27, -72, 7),
        (14, -48, 8),
        (54, -24, 9),
        (54, 24, 10),
        (54, 72, 11),
        (14, 96, 12),
        (-27, 120, 13),
        (-68, 96, 14),
        (-108, 72, 15),
        (-108, 24, 16),
        (-108, -24, 17),
        (-68, -48, 18),
    ]
    horizontal_button_positions = [
        (-148, 0, 19),
        (-108, 24, 20),
        (-68, 0, 21),
        (-27, 24, 22),
        (14, 0, 23),
        (54, 24, 24),
        (94, 0, 25),
    ]
    standard_buttons = {
        0: "copy",
        1: "cut",
        2: "paste",
        3: "line_copy",
        4: "undo",
        5: "redo",
        6: "line_duplicate",
        7: "line_transpose",
        8: "line_cut",
        9: "line_delete",
        10: "select_all",
        11: "special_to_uppercase",
        12: "special_to_lowercase",
        13: "show_edge",
        14: "toggle_line_endings",
        15: "goto_to_end",
        16: "goto_to_start",
        17: "special_indent_to_cursor",
        18: "reset_zoom",
    }
    # A Copy for when the functions need to be reset
    stored_standard_buttons = dict(standard_buttons) # or standard_buttons[:]
    special_buttons = {
        0: "copy",
        1: "cut",
        2: "paste",
        3: "line_copy",
        4: "undo",
        5: "redo",
        6: "line_duplicate",
        7: "line_transpose",
        8: "line_cut",
        9: "line_delete",
        10: "select_all",
        11: "special_to_uppercase",
        12: "special_to_lowercase",
        13: "comment_uncomment",
        14: "toggle_line_endings",
        15: "goto_to_end",
        16: "goto_to_start",
        17: "special_indent_to_cursor",
        18: "create_node_tree",
    }
    # A Copy for when the functions need to be reset
    stored_special_buttons = dict(special_buttons) # or special_buttons[:]
    horizontal_buttons = {
        19: "copy",
        20: "cut",
        21: "paste",
        22: "comment_uncomment",
        23: "undo",
        24: "redo",
        25: "line_duplicate",
    }
    # A Copy for when the functions need to be reset
    stored_horizontal_buttons = dict(horizontal_buttons) # or horizontal_buttons[:]
    # Button scaling factor
    x_scale = 0.7
    y_scale = 0.7
    # Total button position offset
    total_offset = (0, -48)
    # Current context menu functions type
    functions_type = None
    
    def __init__(self, parent=None, main_form=None, offset=(0, 0)):
        # Initialize the superclass
        super().__init__(parent)
        # Store the reference to the parent
        self.setParent(parent)
        # Store the reference to the main form
        self.main_form = main_form
        # Set default font
        self.setFont(data.get_current_font())
        # Store the painting offset
        self.offset = offset
        style_sheet = "background-color: transparent;" + "border: 0 px;"
        self.setStyleSheet(style_sheet)
        # Set the groupbox size
        screen_resolution = data.application.desktop().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.setGeometry(
            functions.create_rect(0, 0, width, height)
        )
    
    @staticmethod
    def reset_functions():
        """
        Copy stored functions back into the active menu functions
        """
        ContextMenu.standard_buttons = dict(ContextMenu.stored_standard_buttons)
        ContextMenu.special_buttons = dict(ContextMenu.stored_special_buttons)
        ContextMenu.horizontal_buttons = dict(ContextMenu.stored_horizontal_buttons)
    
    @staticmethod
    def get_settings():
        """
        Return the custom function settings for the settings manipulator
        """
        return {
            "standard_buttons": ContextMenu.standard_buttons,
            "special_buttons": ContextMenu.special_buttons,
            "horizontal_buttons": ContextMenu.horizontal_buttons,
        }
    
    def check_position_offset(self, 
                              inner_buttons=True, 
                              outer_buttons=True,
                              horizontal_buttons=False):
        button_positions = []
        if inner_buttons == True:
            button_positions.extend(ContextMenu.inner_button_positions)
        if outer_buttons == True:
            button_positions.extend(ContextMenu.outer_button_positions)
        if horizontal_buttons == True:
            button_positions.extend(self.horizontal_button_positions)
        hex_x_size = self.ContextButton.HEX_IMAGE_SIZE[0] * self.x_scale
        hex_y_size = self.ContextButton.HEX_IMAGE_SIZE[1] * self.y_scale
        window_size = self.parent().size() - functions.create_size(hex_x_size, hex_y_size)
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        for b in button_positions:
            x = self.offset[0]+ b[0]*self.x_scale/0.8 + self.total_offset[0]
            y = self.offset[1]+ b[1]*self.y_scale/0.8 + self.total_offset[1]
            if x < min_x:
                min_x = x
            if x > window_size.width():
                new_max = x - window_size.width()
                if new_max > max_x:
                    max_x = new_max
            if y < min_y:
                min_y = y
            if y > window_size.height():
                new_max = y - window_size.height()
                if new_max > max_y:
                    max_y = new_max
        if min_x != 0:
            self.offset = (self.offset[0]-min_x, self.offset[1])
        if max_x != 0:
            self.offset = (self.offset[0]-max_x, self.offset[1])
        if min_y != 0:
            self.offset = (self.offset[0], self.offset[1]-min_y)
        if max_y != 0:
            self.offset = (self.offset[0], self.offset[1]-max_y)
    
    @staticmethod
    def add_function(name, pixmap, function, function_name):
        ContextMenu.function_list[name] = (pixmap, function, function_name)
    
    def mousePressEvent(self, event):
        button = event.button()
        super().mousePressEvent(event)
        self.hide()
    
    def add_buttons(self, buttons):
        """
        Add buttons to the context menu
        """
        total_offset = self.total_offset
        for b in buttons:
            function_info = b[0]
            button_position = b[1]
            button_number = button_position[2]
            button = self.ContextButton(
                self, 
                self.main_form, 
                input_pixmap=function_info[0], 
                input_function=function_info[1], 
                input_function_text=function_info[2],
                input_focus_last_widget=data.HexButtonFocus.TAB,
                input_scale=(self.x_scale, self.y_scale),
            )
            button.number = button_number
            #Set the button size and location
            button.set_offset(
                (self.offset[0]+ button_position[0]*self.x_scale/0.8 + total_offset[0], 
                    self.offset[1]+ button_position[1]*self.y_scale/0.8 + total_offset[1])
            )
            button.dim()
            self.button_list.append(button)
    
    def create_horizontal_multiline_repl_buttons(self):
        # Check if any of the buttons are out of the window and adjust the offset
        self.check_position_offset(
            inner_buttons=False, 
            outer_buttons=False,
            horizontal_buttons=True
        )
        buttons = [ContextMenu.horizontal_buttons[x] for x in range(19, 26)]
        # Add the buttons
        self.button_list = []
        self.add_horizontal_buttons(buttons)
        self.functions_type = "horizontal"
    
    def create_multiline_repl_buttons(self):
        inner_buttons = [ContextMenu.horizontal_buttons[x] for x in range(19, 26)]
        self.create_buttons(inner_buttons)
        self.functions_type = "horizontal"
    
    def create_plain_buttons(self):
        inner_buttons = [ContextMenu.standard_buttons[x] for x in range(7)]
        self.create_buttons(inner_buttons)
        self.functions_type = "plain"
    
    def create_standard_buttons(self):
        inner_buttons = [ContextMenu.standard_buttons[x] for x in range(7)]
        outer_buttons = [ContextMenu.standard_buttons[x] for x in range(7, len(ContextMenu.standard_buttons))]
        self.create_buttons(inner_buttons, outer_buttons)
        self.functions_type = "standard"
    
    def create_special_buttons(self):
        inner_buttons = [ContextMenu.special_buttons[x] for x in range(7)]
        outer_buttons = [ContextMenu.special_buttons[x] for x in range(7, len(ContextMenu.standard_buttons))]
        self.create_buttons(inner_buttons, outer_buttons)
        self.functions_type = "special"
    
    def create_buttons(self, 
                       inner_buttons=[], 
                       outer_buttons=[]):
        # Check if any of the buttons are out of the window and adjust the offset
        if outer_buttons == []:
            self.check_position_offset(
                inner_buttons=True, 
                outer_buttons=False,
                horizontal_buttons=False
            )
        else:
            self.check_position_offset()
        # Add the buttons
        self.button_list = []
        if inner_buttons != []:
            buttons = inner_buttons
            self.add_inner_buttons(buttons)
        if outer_buttons != []:
            buttons = outer_buttons
            self.add_outer_buttons(outer_buttons)
    
    def add_inner_buttons(self, in_buttons):
        self._add_buttons(in_buttons, 7, ContextMenu.inner_button_positions)
    
    def add_outer_buttons(self, in_buttons):
        self._add_buttons(in_buttons, 12, ContextMenu.outer_button_positions)
    
    def add_horizontal_buttons(self, in_buttons):
        self._add_buttons(in_buttons, 7, ContextMenu.horizontal_button_positions)
    
    def _add_buttons(self, in_buttons, max_count, positions):
        if len(in_buttons) > max_count:
            raise Exception("Too many inner buttons in context menu!")
        buttons = []
        for i,button in enumerate(in_buttons):
            if button not in self.function_list:
                self.main_form.display.repl_display_message(
                    f"'{button}' context menu function does not exist!",
                    message_type=data.MessageType.ERROR,
                )
            else:
                buttons.append(
                    (ContextMenu.function_list[button], positions[i])
                )
        self.add_buttons(buttons)
    
    def show(self):
        super().show()
        # When the context menu is shown it is needed to paint
        # the background or the backgrounds will be transparent
        for button in self.button_list:
            button.setVisible(True)
            button._fill_background_color()



