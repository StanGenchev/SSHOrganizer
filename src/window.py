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

from gi import require_version
require_version('Vte', '2.91')
from gi.repository import Gtk, Gdk, Vte, GLib
from .modules.custom_widgets import ConnectionListRow, GroupListRow
from .modules.custom_widgets import FileFolderListRow, TabWidget
from .dialogs.group import GroupWindow
from .dialogs.about import AboutWindow
from .dialogs.connection import ConnectionWindow
from .modules import models, queries

@Gtk.Template(resource_path='/org/gnome/SSHOrganizer/window.ui')
class SshorganizerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'main_window'

    main_window = Gtk.Template.Child()

    # window header widgets
    headerbar_hbox = Gtk.Template.Child()
    left_view_headerbar = Gtk.Template.Child()
    headerbar_separator = Gtk.Template.Child()
    right_view_headerbar = Gtk.Template.Child()
    back_btn = Gtk.Template.Child()
    search_btn = Gtk.Template.Child()
    connect_btn = Gtk.Template.Child()
    add_terminal_btn = Gtk.Template.Child()

    # Popup widgets
    ssh_accounts_btn = Gtk.Template.Child()
    add_group_btn = Gtk.Template.Child()
    remove_group_btn = Gtk.Template.Child()
    theme_btn = Gtk.Template.Child()
    about_btn = Gtk.Template.Child()
    add_conn_btn = Gtk.Template.Child()
    remove_conn_btn = Gtk.Template.Child()
    select_all_conn_btn = Gtk.Template.Child()
    start_sel_btn = Gtk.Template.Child()
    stop_sel_btn = Gtk.Template.Child()
    add_file_folder_btn = Gtk.Template.Child()
    select_all_files_btn = Gtk.Template.Child()
    remove_sel_file_folder_btn = Gtk.Template.Child()

    # window body widgets
    body_hbox = Gtk.Template.Child()
    body_separator = Gtk.Template.Child()

    # connections pane widgets
    left_view_stack = Gtk.Template.Child()
    search_revealer = Gtk.Template.Child()
    group_listbox = Gtk.Template.Child()
    conn_listbox = Gtk.Template.Child()

    # right view widgets
    right_view_scroll = Gtk.Template.Child()
    right_view_viewport = Gtk.Template.Child()
    right_view_stack = Gtk.Template.Child()
    group_details_hbox = Gtk.Template.Child()
    conn_details_hbox = Gtk.Template.Child()
    group_desc_textview = Gtk.Template.Child()
    group_prop_listview = Gtk.Template.Child()
    group_title_entry = Gtk.Template.Child()
    conn_prop_listview = Gtk.Template.Child()
    conn_files_listview = Gtk.Template.Child()
    user_property_value = Gtk.Template.Child()
    pass_property_value = Gtk.Template.Child()
    host_property_value = Gtk.Template.Child()
    port_property_value = Gtk.Template.Child()
    ssh_args_entry = Gtk.Template.Child()
    commands_entry = Gtk.Template.Child()
    group_stack = Gtk.Template.Child()
    conn_type_combobox = Gtk.Template.Child()
    terminals = Gtk.Template.Child()
    ports_box = Gtk.Template.Child()
    ports_label = Gtk.Template.Child()

    # Buffers, ListStores, etc
    group_desc_buffer = Gtk.TextBuffer()
    conn_type_store = Gtk.ListStore(str)

    mobile_view = False
    last_width = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect_signals()
        self.config_widgets()
        self.load_groups()

    def connect_signals(self):
        self.main_window.connect("size-allocate", self.on_size_allocate)
        self.conn_listbox.connect("row-activated", self.on_connection_selected)
        self.theme_btn.connect("clicked", self.on_theme_change)
        self.search_btn.connect("clicked", self.on_search_btn_clicked)
        self.back_btn.connect("clicked", self.on_back_btn_clicked)
        self.group_listbox.connect("row-selected", self.on_group_selected)
        self.right_view_stack.connect("notify", self.on_stack_change)
        self.group_stack.connect("notify", self.on_stack_change)
        self.add_terminal_btn.connect("clicked", self.add_terminal)
        self.add_group_btn.connect("clicked", self.group_dialog)
        self.remove_group_btn.connect("clicked", self.remove_group)
        self.about_btn.connect("clicked", self.about_dialog)
        self.add_conn_btn.connect("clicked", self.connection_dialog)

    def config_widgets(self):
        self.add_terminal_btn.hide()
        self.conn_listbox.set_header_func(self.add_separators, None)
        self.group_prop_listview.set_header_func(self.add_separators, None)
        self.conn_prop_listview.set_header_func(self.add_separators, None)
        self.conn_files_listview.set_header_func(self.add_separators, None)
        self.group_desc_textview.set_buffer(self.group_desc_buffer)
        self.group_desc_buffer.set_text("Description")

    def add_separators(self, row, before, user_data):
        if before and not row.get_header():
            row.set_header(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

    def group_dialog(self, button):
        dialog = GroupWindow(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            name = dialog.name_entry.get_text()
            desc = dialog.desc.get_text(dialog.desc.get_start_iter(),
                                        dialog.desc.get_end_iter(),
                                        include_hidden_chars=True)
            try:
                queries.add_group(name, desc)
            except Exception:
                msg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                    Gtk.ButtonsType.OK, "Could not create group!")
                msg.format_secondary_text(
                    "An error occurred when creating group '" + name + "'")
                msg.run()
                msg.destroy()

        dialog.destroy()
        self.clear_listbox(self.group_listbox)
        self.load_groups()

    def connection_dialog(self, button):
        dialog = ConnectionWindow(self,
                                  queries.get_account(None),
                                  queries.get_session_type(None))
        response = dialog.run()

        group = self.group_listbox.get_selected_row().group_id
        if response == Gtk.ResponseType.OK:
            name = dialog.name_entry.get_text()
            host = dialog.host_entry.get_text()
            port = dialog.port_entry.get_text()
            account = dialog.account_combobox.get_active_id()
            username = dialog.user_entry.get_text()
            password = dialog.pass_entry.get_text()
            session_type = dialog.conn_type_combobox.get_active_id()

            # try:
            if account != 'custom':
                acc = queries.get_account(account)[0]
                username = acc.name
                password = acc.password
            queries.add_connection(name,
                                   host,
                                   port,
                                   username,
                                   password,
                                   group,
                                   session_type)
            # except Exception:
            #     msg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            #         Gtk.ButtonsType.OK, "Could not create connection!")
            #     msg.format_secondary_text(
            #         "An error occurred when creating connection '" + name + "'")
            #     msg.run()
            #     msg.destroy()

        dialog.destroy()
        self.clear_listbox(self.conn_listbox)
        self.load_connections(group)

    def about_dialog(self, button):
        dialog = AboutWindow(self)
        dialog.run()
        dialog.destroy()

    def load_groups(self):
        groups = queries.get_group(None)
        for group in groups:
            row = GroupListRow(group.name, group.description, group.id)
            self.group_listbox.add(row)
        self.group_listbox.show_all()
        first_row = self.group_listbox.get_row_at_index(0)
        self.group_listbox.select_row(first_row)

    def remove_group(self, button):
        row = self.group_listbox.get_selected_row()
        queries.delete_group(row.group_id)
        self.clear_listbox(self.group_listbox)
        self.load_groups()
        first_row = self.group_listbox.get_row_at_index(0)
        self.group_listbox.select_row(first_row)

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
        self.terminals.append_page_menu(terminal, tab, Gtk.Label("Local"))
        self.terminals.show_all()

    def on_add_connection_clicked(self, button):
        self.add_conn_dialog.show_all()

    def on_cancel_new_conn_btn_clicked(self, button):
        self.add_conn_dialog.hide()

    def on_remove_connection_clicked(self, button):
        pass

    def on_tab_close_clicked(self, button, tab):
        pagenum = self.terminals.page_num(tab)
        self.terminals.remove_page(pagenum)

    def on_search_btn_clicked(self, button):
        if self.search_revealer.get_reveal_child():
            self.search_revealer.set_reveal_child(False)
        else:
            self.search_revealer.set_reveal_child(True)

    def on_theme_change(self, button):
        settings = Gtk.Settings.get_default()
        if settings.get_property("gtk-application-prefer-dark-theme"):
            settings.set_property("gtk-application-prefer-dark-theme", False)
            button.set_property("text", "Dark theme")
        else:
            settings.set_property("gtk-application-prefer-dark-theme", True)
            button.set_property("text", "Light theme")

    def on_back_btn_clicked(self, button):
        if self.group_stack.get_visible_child_name() == "conn_details":
            self.group_stack.set_visible_child_name("group_details")
            if not self.mobile_view:
                button.hide()
        else:
            if self.mobile_view:
                self.left_view_stack.set_visible_child_name("groups_list")
                self.left_view_headerbar.show()
                self.right_view_headerbar.hide()

    def on_group_selected(self, widget, row):
        if row is not None:
            self.group_title_entry.set_text(row.label.get_text())
            self.group_desc_buffer.set_text(row.desc)
            self.clear_listbox(self.conn_listbox)
            self.load_connections(row.group_id)
            if self.mobile_view:
                self.left_view_headerbar.hide()
                self.right_view_headerbar.show()
                self.back_btn.show()
                self.left_view_stack.set_visible_child(self.right_view_stack)
            self.right_view_stack.set_visible_child_name("details_page")
            self.group_stack.set_visible_child_name("group_details")

    def clear_listbox(self, listbox):
        for index in range(len(listbox)-1, -1, -1):
            listbox.remove(listbox.get_row_at_index(index))

    def load_connections(self, gid):
        connections = queries.get_connection(None, gid)
        for item in connections:
            row = ConnectionListRow(item.name, item.id)
            self.conn_listbox.add(row)
        self.conn_listbox.show_all()

    def on_connection_selected(self, widget, row):
        self.group_stack.set_visible_child_name("conn_details")
        self.back_btn.show()
        if self.mobile_view:
            self.left_view_headerbar.hide()
            self.headerbar_separator.hide()
            self.right_view_headerbar.show()

        connection = queries.get_connection(row.conn_id, None)[0]
        self.user_property_value.set_text(connection.user)
        self.pass_property_value.set_text(connection.password)
        self.host_property_value.set_text(connection.host)
        self.port_property_value.set_text(str(connection.port))

        types = queries.get_session_type(None)
        for t in types:
            self.conn_type_combobox.append(str(t.id), t.name)
        self.conn_type_combobox.set_active_id(str(connection.session_type.id))

        self.clear_listbox(self.conn_files_listview)
        file_folders = queries.get_file_folder(None, connection.id)
        for ff in file_folders:
            row = FileFolderListRow(ff.source, ff.id)
            self.conn_files_listview.add(row)
        self.conn_files_listview.show_all()

        self.ssh_args_entry.set_text(connection.arguments)
        self.commands_entry.set_text(connection.commands)

    def on_stack_change(self, stack, param):
        if param.name == "transition-running":
            if stack.get_visible_child_name() == "terminals_page":
                self.add_terminal_btn.show()
                if self.mobile_view:
                    self.back_btn.show()
                else:
                    self.back_btn.hide()
            if stack.get_visible_child_name() == "details_page":
                self.add_terminal_btn.hide()
                child = stack.get_child_by_name("details_page")
                if child.get_visible_child_name() == "group_details":
                    if self.mobile_view:
                        self.back_btn.show()
                    else:
                        self.back_btn.hide()
                else:
                    self.back_btn.show()

    def on_size_allocate(self, *args):
        width, _ = self.main_window.get_size()
        if self.last_width != width:
            self.last_width = width
            if width >= 895:
                self.group_details_hbox.set_size_request(600, -1)
                self.group_details_hbox.set_halign(Gtk.Align.CENTER)
                self.conn_details_hbox.set_size_request(600, -1)
                self.conn_details_hbox.set_halign(Gtk.Align.CENTER)
            else:
                self.group_details_hbox.set_size_request(-1, -1)
                self.group_details_hbox.set_halign(Gtk.Align.FILL)
                self.conn_details_hbox.set_size_request(-1, -1)
                self.conn_details_hbox.set_halign(Gtk.Align.FILL)
            if width <= 720:
                if not self.mobile_view:
                    self.right_view_headerbar.hide()
                    self.headerbar_separator.hide()
                    self.left_view_headerbar.set_show_close_button(True)
                    self.headerbar_hbox.set_homogeneous(True)
                    self.right_view_stack.reparent(self.left_view_stack)
                    self.body_separator.hide()
                    self.right_view_scroll.hide()
                    self.body_hbox.set_homogeneous(True)
                    self.mobile_view = True
            elif self.mobile_view:
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
