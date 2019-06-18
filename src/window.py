#!/usr/bin/env python3
# window.py
#
# Copyright 2019 StanGenchev
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.

import os
import sys

# files = []

# for r, d, f in os.walk(os.path.dirname(os.path.realpath(__file__))):
#     for file in f:
#         files.append(os.path.join(r, file))

# for f in files:
#     print(f)

from gi import require_version
require_version('Vte', '2.91')
from gi.repository import Gtk, Gdk, Vte, GLib
from .modules.custom_widgets import ConnectionListRow, GroupListRow, TabWidget
from .dialogs.group import GroupWindow

@Gtk.Template(resource_path='/org/gnome/SSHOrganizer/window.ui')
class SshorganizerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'SshorganizerWindow'

    SshorganizerWindow = Gtk.Template.Child()

    # window header widgets
    headerbar_hbox = Gtk.Template.Child()
    left_view_headerbar = Gtk.Template.Child()
    headerbar_separator = Gtk.Template.Child()
    right_view_headerbar = Gtk.Template.Child()
    back_button = Gtk.Template.Child()
    search_conn_button = Gtk.Template.Child()
    settings_button = Gtk.Template.Child()
    connect_button = Gtk.Template.Child()
    add_terminal_button = Gtk.Template.Child()

    # Popup widgets
    add_group_button = Gtk.Template.Child()

    # window body widgets
    body_hbox = Gtk.Template.Child()
    body_separator = Gtk.Template.Child()

    # connections pane widgets
    left_view_stack = Gtk.Template.Child()
    search_revealer = Gtk.Template.Child()
    group_list_scrollview = Gtk.Template.Child()
    group_listbox = Gtk.Template.Child()
    conn_listbox = Gtk.Template.Child()

    # right view widgets
    right_view_scroll = Gtk.Template.Child()
    right_view_viewport = Gtk.Template.Child()
    right_view_stack = Gtk.Template.Child()
    conn_details_scroll = Gtk.Template.Child()
    group_details_scroll = Gtk.Template.Child()
    group_title_entry = Gtk.Template.Child()
    user_property_value = Gtk.Template.Child()
    host_property_value = Gtk.Template.Child()
    port_property_value = Gtk.Template.Child()
    group_conn_stack = Gtk.Template.Child()
    terminals_container = Gtk.Template.Child()

    # Buffers, ListStores, etc
    group_desc_textbuffer = Gtk.Template.Child()

    mobile_view = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect_signals()
        self.config_widgets()
        self.add_groups()

    def connect_signals(self):
        self.SshorganizerWindow.connect("size-allocate", self.on_size_allocate)
        self.conn_listbox.connect("row-activated", self.on_connection_selected)
        #self.change_theme_button.connect("clicked", self.on_theme_change)
        self.search_conn_button.connect("clicked", self.on_search_conn_button_clicked)
        self.back_button.connect("clicked", self.on_back_button_clicked)
        self.group_listbox.connect("row-selected", self.on_group_selected)
        self.right_view_stack.connect("notify", self.on_stack_change)
        self.add_terminal_button.connect("clicked", self.add_terminal)
        self.add_group_button.connect("clicked", self.group_dialog)

    def config_widgets(self):
        self.connect_button.hide()
        self.add_terminal_button.hide()
        self.conn_listbox.set_header_func(self.list_header_func, None)

    def list_header_func(self, row, before, user_data):
        if before and not row.get_header():
            row.set_header(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

    def group_dialog(self, button):
        GroupWindow(self)

    def add_groups(self):
        items = 'Quanterall Aeternity Wine-HRS CollectionTech'.split()
        for i, item in enumerate(items):
            row = GroupListRow(item, i)
            self.group_listbox.add(row)
        self.group_listbox.show_all()

    def add_terminal(self, button):
        command = "echo 'Hello World'\n"
        terminal = Vte.Terminal()
        terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["/bin/bash"],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            )
        command_decimal = []
        for c in command:
            command_decimal.append(ord(c))
        terminal.feed_child(command_decimal)
        tab = TabWidget("Local")
        tab.button.connect("clicked", self.on_tab_close_clicked, tab)
        self.terminals_container.append_page_menu(terminal, tab, Gtk.Label("Local"))
        self.terminals_container.show_all()

    def on_add_connection_clicked(self, button):
        self.add_conn_dialog.show_all()

    def on_cancel_new_conn_button_clicked(self, button):
        self.add_conn_dialog.hide()

    def on_remove_connection_clicked(self, button):
        pass

    def on_tab_close_clicked(self, button, tab):
        pagenum = self.terminals_container.page_num(tab)
        self.terminals_container.remove_page(pagenum)

    def on_search_conn_button_clicked(self, button):
        if self.search_revealer.get_reveal_child():
            self.search_revealer.set_reveal_child(False)
        else:
            self.search_revealer.set_reveal_child(True)

    def on_group_combo_change(self, button):
        pass

    def on_theme_change(self, button):
        settings = Gtk.Settings.get_default()
        if settings.get_property("gtk-application-prefer-dark-theme"):
            settings.set_property("gtk-application-prefer-dark-theme", False)
            button.set_property("text", "Dark theme")
        else:
            settings.set_property("gtk-application-prefer-dark-theme", True)
            button.set_property("text", "Light theme")

    def on_back_button_clicked(self, button):
        if self.group_conn_stack.get_visible_child_name() == "conn_details":
            self.group_conn_stack.set_visible_child(self.group_details_scroll)
            if not self.mobile_view:
                self.back_button.hide()
        else:
            if self.mobile_view:
                self.left_view_stack.set_visible_child_name("groups_list")
                self.left_view_headerbar.show()
                self.right_view_headerbar.hide()

    def on_group_selected(self, widget, row):
        self.group_title_entry.set_text(row.label.get_text())
        self.group_desc_textbuffer.set_text(row.demo_desk)
        for index in range(len(self.conn_listbox)-1, -1, -1):
            self.conn_listbox.remove(self.conn_listbox.get_row_at_index(index))
        items = 'First Second Third'.split()
        for item in items:
            row = ConnectionListRow(item)
            self.conn_listbox.add(row)
        self.conn_listbox.show_all()
        if self.mobile_view:
            self.left_view_headerbar.hide()
            self.right_view_headerbar.show()
            self.back_button.show()
            self.left_view_stack.set_visible_child(self.right_view_stack)
        self.right_view_stack.set_visible_child_name("details_page")

    def on_connection_selected(self, parent, child):
        self.group_conn_stack.set_visible_child(self.conn_details_scroll)
        self.user_property_value.set_text(child.label.get_text())
        self.host_property_value.set_text("192.168.0.2")
        self.port_property_value.set_text("22")
        self.back_button.show()
        if self.mobile_view:
            self.left_view_headerbar.hide()
            self.headerbar_separator.hide()
            self.right_view_headerbar.show()

    def on_stack_change(self, stack, param):
        if param.name == "transition-running":
            if stack.get_visible_child_name() == "terminals_page":
                self.add_terminal_button.show()
                self.connect_button.hide()
                if self.mobile_view:
                    self.back_button.show()
                else:
                    self.back_button.hide()
            if stack.get_visible_child_name() == "details_page":
                self.add_terminal_button.hide()
                if stack.get_child_by_name("details_page").get_visible_child_name() == "group_details":
                    self.connect_button.hide()
                    if self.mobile_view:
                        self.back_button.show()
                    else:
                        self.back_button.hide()
                else:
                    self.connect_button.show()
                    self.back_button.show()

    def on_size_allocate(self, *args):
        width, _ = self.SshorganizerWindow.get_size()
        if width <= 720:
            self.back_button.show()
            if self.right_view_stack.get_parent().get_name() != "GtkStack":
                self.right_view_headerbar.hide()
                self.headerbar_separator.hide()
                self.left_view_headerbar.set_show_close_button(True)
                self.headerbar_hbox.set_homogeneous(True)
                self.right_view_stack.reparent(self.left_view_stack)
                self.body_separator.hide()
                self.right_view_scroll.hide()
                self.body_hbox.set_homogeneous(True)
                self.mobile_view = True
        else:
            self.back_button.hide()
            if self.right_view_stack.get_parent().get_name() == "GtkStack":
                self.right_view_headerbar.show()
                self.headerbar_separator.show()
                self.left_view_headerbar.set_show_close_button(False)
                self.headerbar_hbox.set_homogeneous(False)
                self.right_view_stack.reparent(self.right_view_viewport)
                self.body_separator.show()
                self.right_view_scroll.show()
                self.body_hbox.set_homogeneous(False)
                self.left_view_headerbar.show()
                self.headerbar_separator.show()
                self.right_view_headerbar.show()
                self.mobile_view = False
