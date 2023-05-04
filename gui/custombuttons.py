
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
-----------------------------------------------------------------------------------
Custom buttons used by the FunctionWheel and ContextMenu in the forms module
-----------------------------------------------------------------------------------
"""
class CustomButton(data.QLabel):
    """
    Custom button used for displaying and executing Ex.Co. functions
    """
    #Class variables
    parent              = None
    group_box_parent    = None
    main_form           = None
    stored_pixmap       = None
    stored_font         = None
    stored_hex          = None
    function            = None
    function_text       = None
    stored_opacity      = 0.0
    focus_last_widget   = True
    no_tab_focus_disable       = False
    no_document_focus_disable  = True
    check_last_tab_type = False
    check_text_differ   = None
    tool_tip            = None
    scale               = (1, 1)
    # Class constants
    OPACITY_LOW         = 0.5
    OPACITY_HIGH        = 1.0
    """
    This was measured by hand
    """
    INNER_IMAGE_OFFSET  = (18, 13)
    """
    This should be the actual pixel dimensions of the hex image file
    """
    HEX_IMAGE_SIZE      = (68, 60)
    
    
    def __init__(self, 
                 parent, 
                 main_form,
                 input_pixmap, 
                 input_function=None, 
                 input_function_text="", 
                 input_font=data.QFont(
                 'Courier', 14, weight=data.QFont.Bold
                 ), 
                 input_focus_last_widget=data.HexButtonFocus.NONE, 
                 input_no_tab_focus_disable=False, 
                 input_no_document_focus_disable=True, 
                 input_check_last_tab_type=False, 
                 input_check_text_differ=False, 
                 input_tool_tip=None,
                 input_scale=(1, 1)):
        #Initialize superclass
        super().__init__(parent)
        #Store the reference to the parent
        self._parent = parent
        #Store the reference to the main form
        self.main_form = main_form
        # Set default font
        self.setFont(data.get_current_font())
        #Store the reference to the group box that holds the parent
        #(the parent of the parent)
        self.group_box_parent = parent.parent
        #Store the main function image
        self.stored_pixmap = input_pixmap
        #Store the hex edge image
        self.stored_hex = data.QPixmap(
            os.path.join(
                data.resources_directory, 
                "various/hex-button-edge.png"
            )
        )
        #Store the function that will be executed on the click event
        self.function = input_function
        #Store the function text
        self.function_text = input_function_text
        #Set the attribute that will be check if focus update is needed
        #when the custom button executes its function
        self.focus_last_widget = input_focus_last_widget
        #Set the attribute that checks if any tab is focused
        self.no_tab_focus_disable = input_no_tab_focus_disable
        #Set the attribute that will be check if button will be disabled
        #if there is no focused document tab
        self.no_document_focus_disable = input_no_document_focus_disable
        #Set checking the save state stored in the main form
        self.check_last_tab_type = input_check_last_tab_type
        #Set checking for if the focused tab is a text differer
        self.check_text_differ = input_check_text_differ
        #Set the font that will be used with the button
        self.stored_font = input_font
        #Enable mouse move events
        self.setMouseTracking(True)
        #Set the image for displaying
#        self.setPixmap(input_pixmap)
#        #Image should scale to the button size
#        self.setScaledContents(True)
#        # Set the button mask, which sets the button area to the shape of
#        # the button image instead of a rectangle
#        self.setMask(self.stored_hex.mask())
#        #Set the initial opacity to low
#        self._set_opacity_with_hex_edge(self.OPACITY_LOW)
        #Set the tooltip if it was set
        if input_tool_tip != None:
            self.setToolTip(input_tool_tip)
        # Set the scaling
        self.scale = input_scale

    def _set_opacity(self, input_opacity):
        """Set the opacity of the stored QPixmap image and display it"""
        # Store the opacity
        self.stored_opacity = input_opacity
        # Create and initialize the QImage from the stored QPixmap
        button_image = self.stored_pixmap
        # Resize the button image to scale
        button_image = button_image.scaled(
            functions.create_size(
                math.ceil(button_image.size().width() * self.scale[0]),
                math.ceil(button_image.size().height() * self.scale[1]),
            ),
            transformMode=data.Qt.SmoothTransformation
        )
        # Scale the hex image
        hex_image = self.stored_hex
        scaled_size = functions.create_size(
            math.ceil(hex_image.size().width() * self.scale[0]),
            math.ceil(hex_image.size().height() * self.scale[1]),
        )
        image = data.QImage(
            scaled_size, #hex_image.size(), 
            data.QImage.Format_ARGB32_Premultiplied
        )
        image.fill(data.Qt.transparent)
        # Create and initialize the QPainter that will manipulate the QImage
        button_painter = data.QPainter(image)
        button_painter.setOpacity(input_opacity)
        # Adjust inner button positioning according to the scale
        x_scaled = math.ceil(self.scale[0] * self.INNER_IMAGE_OFFSET[0])
        y_scaled = math.ceil(self.scale[1] * self.INNER_IMAGE_OFFSET[1])
        button_painter.drawPixmap(x_scaled, y_scaled, button_image)
        button_painter.end()
        # Display the manipulated image
        self.setPixmap(data.QPixmap.fromImage(image))
        # Set the button mask, which sets the button area to the shape of
        # the button image instead of a rectangle
        self.setMask(hex_image.mask())
    
    def _set_opacity_with_hex_edge(self, input_opacity):
        """
        Set the opacity of the stored QPixmap image and display it
        """
        # Store the opacity
        self.stored_opacity = input_opacity
        # Create and initialize the QImage from the stored QPixmap
        button_image = self.stored_pixmap
        # Resize the button image to scale
        button_image = button_image.scaled(
            functions.create_size(
                math.ceil(button_image.size().width() * self.scale[0]),
                math.ceil(button_image.size().height() * self.scale[1]),
            ),
            transformMode=data.Qt.SmoothTransformation
        )        
        # Scale the hex image
        hex_image = self.stored_hex
        scaled_size = functions.create_size(
            math.ceil(hex_image.size().width() * self.scale[0]),
            math.ceil(hex_image.size().height() * self.scale[1]),
        )
        image = data.QImage(
            scaled_size,
            data.QImage.Format_ARGB32_Premultiplied,
        )
        image.fill(data.Qt.transparent)
#        image.fill(data.theme.Context_Menu_Background)
        # Create and initialize the QPainter that will manipulate the QImage
        button_painter = data.QPainter(image)
        button_painter.setCompositionMode(
            data.QPainter.CompositionMode_SourceOver
        )
        button_painter.setOpacity(input_opacity)
        # Resize the hex image to scale
        hex_image = hex_image.scaled(
            functions.create_size(
                math.ceil(hex_image.size().width() * self.scale[0]),
                math.ceil(hex_image.size().height() * self.scale[1]),
            ),
            transformMode=data.Qt.SmoothTransformation
        )
        # Adjust inner button positioning according to the scale
        button_painter.drawPixmap(0, 0, hex_image)
        x_scaled = math.ceil(self.scale[0] * self.INNER_IMAGE_OFFSET[0])
        y_scaled = math.ceil(self.scale[1] * self.INNER_IMAGE_OFFSET[1])
        button_painter.drawPixmap(x_scaled, y_scaled, button_image)
        button_painter.end()
        # Display the manipulated image
        self.setPixmap(data.QPixmap.fromImage(image))
        # Set the button mask, which sets the button area to the shape of
        # the button image instead of a rectangle
        self.setMask(hex_image.mask())
    
    def set_offset(self, offset):
        self.setGeometry(
            int(offset[0]),
            int(offset[1]),
            math.ceil(self.scale[0] * self.HEX_IMAGE_SIZE[0]), 
            math.ceil(self.scale[0] * self.HEX_IMAGE_SIZE[1])
        )
    
    def mousePressEvent(self, event):
        """Overloaded widget click event"""
        #Execute the superclass mouse click event first
        super().mousePressEvent(event)
        #Execute the function if it was initialized
        if self.function != None:
            try:
                #Set focus to the last focused widget stored on the main form
                if self.focus_last_widget == data.HexButtonFocus.TAB:
                    self.main_form.last_focused_widget.currentWidget().setFocus()
                elif self.focus_last_widget == data.HexButtonFocus.WINDOW:
                    self.main_form.last_focused_widget.setFocus()
                #Store the executed function for next cursor placement
                self.main_form.view.last_executed_function_text = self.function_text
                #Execute the buttons stored function
                self.function()
            except:
                traceback.print_exc()
                message = "You need to focus one of the editor windows first!"
                self.main_form.display.repl_display_message(
                    message, 
                    message_type=data.MessageType.ERROR
                )
            #Close the function wheel
            self._parent.hide()
    
    def mouseMoveEvent(self, event):
        """Overloaded mouse move event"""
        super().mouseMoveEvent(event)
        if self.isEnabled() == True:
            self.highlight()
    
    def enterEvent(self, event):
        """Overloaded widget enter event"""
        super().enterEvent(event)
        #Bring the widget to the front of the Z-axis stack
        self.raise_()
        #Highlight the widget only if it's enabled
        if self.isEnabled() == True:
            self.highlight()
    
    def leaveEvent(self, event):
        """Overloaded widget leave event"""
        super().leaveEvent(event)
        #Dim the widget only if it's enabled
        if self.isEnabled() == True:
            self.dim()
    
    def dim(self, clear_hex_edge=False):
        """Set the buttons opacity to low and clear the function text"""
        #Set the opacity to low
        if clear_hex_edge == True:
            self._set_opacity(self.OPACITY_LOW)
        else:
            self._set_opacity_with_hex_edge(self.OPACITY_LOW)
        #Clear the text in the parent display label
        self._parent.display("", self.stored_font)
    
    def highlight(self):
        """Set the buttons opacity to high and display the buttons function text"""
        #Set the opacity to full
        self._set_opacity_with_hex_edge(self.OPACITY_HIGH)
        #Display the stored function text
        self._parent.display(self.function_text, self.stored_font)


class DoubleButton(CustomButton):
    """
    A CustomButton with an extra button added to itself,
    used for when double functionality is needed, for example when
    a function has a version with or without a dialog window.
    """
    #The extra button reference
    parent                      = None
    main_form                   = None
    extra_button                = None
    extra_button_size_factor    = 1/3
    extra_button_position       = functions.create_point(0, 0)
    extra_button_stored_opacity = None
    extra_button_stored_pixmap  = None
    extra_button_function       = None
    extra_button_function_text  = None
    #Class constants
    OPACITY_LOW                 = 0.5
    OPACITY_HIGH                = 1.0
    
    def init_extra_button(self, 
                          parent, 
                          main_form, 
                          input_extra_pixmap, 
                          input_extra_function=None, 
                          input_extra_function_text=""):   
        #Store the parent and main form references
        self._parent     = parent
        self.main_form  = main_form
        #Initialize the extra button
        self.extra_button = data.QLabel(self)
        width   = int(self.geometry().width() * self.extra_button_size_factor)
        height  = int(self.geometry().height() * self.extra_button_size_factor)
        self.extra_button_position = functions.create_point(
            int(self.geometry().width()*2/3-width),
            int(self.geometry().height()*1/4)
        )
        rectangle = functions.create_rect(
            self.extra_button_position,
            functions.create_size(width, height)
        )
        self.extra_button.setGeometry(rectangle)
        self.extra_button_stored_pixmap = input_extra_pixmap
        self.extra_button.setPixmap(input_extra_pixmap)
        self.extra_button.setScaledContents(True)
        #Store the function options
        self.extra_button_function      = input_extra_function
        self.extra_button_function_text = input_extra_function_text
        #Set the extra button opacity to low
        self._set_extra_button_opacity(self.OPACITY_LOW)
        #Overridden the extra buttons events
        self.extra_button.mousePressEvent   = self.extra_button_click
        self.extra_button.enterEvent        = self.extra_button_enter_event
        self.extra_button.leaveEvent        = self.extra_button_leave_event
    
    def extra_button_click(self, event):
        """mousePressEvent for the extra button"""
        #Execute the function if it was initialized
        if self.extra_button_function is None:
            return
        try:
            #Set focus to the last focused widget stored on the main form
            if self.focus_last_widget == data.HexButtonFocus.TAB:
                self.main_form.last_focused_widget.currentWidget().setFocus()
            elif self.focus_last_widget == data.HexButtonFocus.WINDOW:
                self.main_form.last_focused_widget.setFocus()
            #Store the executed function for next cursor placement
            self.main_form.view.last_executed_function_text = self.function_text
            #Execute the buttons stored function
            self.extra_button_function()
        except Exception as ex:
            print(ex)
            message = "You need to focus one of the editor windows first!"
            self.main_form.display.repl_display_message(
                message, 
                message_type=data.MessageType.ERROR
            )
        #Close the function wheel
        self._parent.hide()
    
    def extra_button_enter_event(self, event):
        """Overloaded widget enter event"""
        #Check if the button is enabled
        if self.isEnabled() == True:
            self._set_extra_button_opacity(self.OPACITY_HIGH)
            #Display the stored extra buttons function text
            extra_button_font = data.QFont(
                data.current_font_name, 
                self.stored_font.pointSize()-2, 
                weight=data.QFont.Bold
            )
            self._parent.display(
                self.extra_button_function_text, 
                extra_button_font
            )
    
    def extra_button_leave_event(self, event):
        """Overloaded widget enter event"""
        #Check if the button is enabled
        if self.isEnabled() == True:
            self._set_extra_button_opacity(self.OPACITY_LOW)
            #Clear the function text
            extra_button_font = data.QFont(
                'Courier', 
                self.stored_font.pointSize()-2, 
                weight=data.QFont.Bold
            )
            self._parent.display(
                "", 
                extra_button_font
            )
    
    def extra_button_enable(self):
        """Hide and disable the extra button"""
        self.extra_button.setVisible(True)
        self.extra_button.setEnabled(True)
    
    def extra_button_disable(self):
        """Hide and disable the extra button"""
        self.extra_button.setVisible(False)
        self.extra_button.setEnabled(False)
        self._set_extra_button_opacity(self.OPACITY_LOW)
    
    def resizeEvent(self, event):
        """Overridden resize event"""
        #Execute the superclass resize function
        super().resizeEvent(event)
        #Update the extra button geometry
        width = int(self.geometry().width() * self.extra_button_size_factor)
        height = int(self.geometry().height() * self.extra_button_size_factor)
        rectangle = functions.create_rect(
            self.extra_button_position, 
            functions.create_size(width, height)
        )
        self.extra_button.setGeometry(rectangle)
    
    def _set_extra_button_opacity(self, input_opacity):
        """Set the opacity of the extra button"""
        #Store the opacity
        self.extra_button_stored_opacity = input_opacity
        #Create and initialize the QImage from the stored QPixmap
        button_image = self.extra_button_stored_pixmap
        image = data.QImage(
            button_image.size(), 
            data.QImage.Format_ARGB32_Premultiplied
        )
        image.fill(data.Qt.transparent)
        #Create and initialize the QPainter that will manipulate the QImage
        button_painter = data.QPainter(image)
        button_painter.setOpacity(input_opacity)
        button_painter.drawPixmap(0, 0, button_image)
        button_painter.end()
        #Display the manipulated image
        self.extra_button.setPixmap(data.QPixmap.fromImage(image))

