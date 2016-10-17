#!/usr/bin/env python
# -*- coding: utf-8 -*- 


from __future__ import unicode_literals
import os
import re

from model.singlenton import Singleton


class ThemeHandler(Singleton):
    def __init__(self):
        self.theme_path = 'resources/theme'
        self.skin_path = 'resources/skin'

        self.theme_name = 'material'
        self.skin_name = 'light'

        self.skin_keys = {
            'file_dialog_background': '',
            'file_dialog_color': '',
            'widget_background': '',
            'widget_color': '',
            'main_window_background': '',
            'tree_widget_background': '',
            'tree_widget_item_background': '',
            'tree_widget_item_alternate_background': '',
            'tree_item_hover_background': '',
            'tree_item_selected_background': '',
            'tree_item_selected_color': '',
            'tree_item_active_background': '',
            'header_view_background': '',
            'header_view_color': '',
            'header_view_item_hover_background': '',
            'vertical_header_background': '',
            'vertical_header_color': '',
            'vertical_header_hover_background': '',
            'menubar_background': '',
            'menubar_border_top_color': '',
            'menubar_item_color': '',
            'menubar_item_selected_background': '',
            'menubar_item_selected_color': '',
            'menubar_item_pressed_background': '',
            'menubar_item_pressed_color': '',
            'menu_background': '',
            'menu_color': '',
            'menu_item_selected_background': '',
            'menu_item_selected_color': '',
            'tool_bar_background': '',
            'button_background': '',
            'button_hover_background': '',
            'button_hover_color': '',
            'button_pressed_background': '',
            'button_pressed_color': '',
            'combobox_background': '',
            'combobox_border_color': '',
            'combobox_font_select_background': '',
            'combobox_font_select_border_color': '',
            'combobox_line_midel_color': '',
            'combobox_panel_background': '',
            'combobox_font_select_item_hover_background': '',
            'combobox_font_select_item_hover_color': '',
            'spinbox_background': '',
            'spinbox_border_color': '',
            'text_edit_background': '',
            'line_edit_background': '',
            'line_edit_border_color': '',
            'tabbar_background': '',
            'tabbar_header_background': '',
            'tabbar_tool_buttons_background': '',
            'tabbar_header_border_top_color': '',
            'tabbar_header_border_right_color': '',
            'tabbar_header_selected_background': '',
            'tabbar_header_selected_border_bottom_color': '',
            'scrollbar_space_border_color': '',
            'scrollbar_space_background': '',
            'scrollbar_background': '',
            'scrollbar_arrow_background': '',
            'control_background': '',
            'about_buttons_area_background': '',
            'plot_main_color': '',
            'plot_signal_area_color': '',
            'plot_background_area_color': '',
            'plot_color': '',
            'plot_background': '',
            'plot_span_selector': '',
            'plot_tool_bar_background': '',
            'plot_tooltip_color': '',
            'plot_tooltip_background': '',
            'stk_left_panel_background': '',
            'stk_buttons_hover_border_color': '',
            'stk_buttons_pressed_border_color': '',
            'stk_right_area_border_color': '',
            'stk_right_area_label_color': '',
        }

        self.theme = None

    def load(self, theme_name, skin_name, font):
        if os.path.exists(os.path.join(self.theme_path, theme_name)):
            self.theme_name = theme_name
        if os.path.exists(os.path.join(self.skin_path, skin_name)):
            self.skin_name = skin_name

        theme_file = open(os.path.join(self.theme_path, theme_name))
        theme_file = theme_file.read()
        skin_file = open(os.path.join(self.skin_path, skin_name))
        skin_file = skin_file.read()

        for key in self.skin_keys:
            pattern = '\n' + key + " = '(.*?)'"
            value = re.findall(pattern, skin_file)
            if value:
                self.skin_keys[key] = value[0]

        self.skin_keys['font_family'] = font[0]
        self.skin_keys['font_size'] = font[1]
        self.skin_keys['font_size_plus'] = str(int(int(font[1])+(int(font[1])*18/100)))
        self.skin_keys['font_style'] = font[2]
        self.skin_keys['font_weight'] = font[3]

        self.theme = theme_file.format(**self.skin_keys)
