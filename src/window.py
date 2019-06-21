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

from datetime import datetime
from gi import require_version
require_version('Vte', '2.91')
from gi.repository import Gtk, Gdk, Vte, GLib
from .modules.custom_widgets import ConnectionListRow, GroupListRow
from .modules.custom_widgets import FileFolderListRow, TabWidget
from .modules.group import GroupWindow
from .modules.about import AboutWindow
from .modules.accounts import AccountWindow
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
    add_file_btn = Gtk.Template.Child()
    add_folder_btn = Gtk.Template.Child()
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
    name_property_value = Gtk.Template.Child()
    user_property_value = Gtk.Template.Child()
    pass_property_value = Gtk.Template.Child()
    host_property_value = Gtk.Template.Child()
    port_property_value = Gtk.Template.Child()
    ssh_args_entry = Gtk.Template.Child()
    commands_entry = Gtk.Template.Child()
    group_stack = Gtk.Template.Child()
    conn_type_combobox = Gtk.Template.Child()
    port_forwarding_frame = Gtk.Template.Child()
    terminals = Gtk.Template.Child()
    account_combobox = Gtk.Template.Child()
    user_property_row = Gtk.Template.Child()
    pass_property_row = Gtk.Template.Child()
    local_port_entry = Gtk.Template.Child()
    remote_port_entry = Gtk.Template.Child()
    conn_files_box = Gtk.Template.Child()
    conn_files_frame = Gtk.Template.Child()

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
        self.main_window.connect("size-allocate", self.size_allocate)
        self.conn_listbox.connect("row-activated", self.connection_selected)
        self.theme_btn.connect("clicked", self.theme_change)
        self.search_btn.connect("clicked", self.search_btn_clicked)
        self.back_btn.connect("clicked", self.back_btn_clicked)
        self.group_listbox.connect("row-selected", self.group_selected)
        self.right_view_stack.connect("notify", self.stack_change)
        self.group_stack.connect("notify", self.stack_change)
        self.group_title_entry.connect("changed", self.group_title_changed)
        self.group_desc_buffer.connect("changed", self.group_desc_changed)
        self.add_terminal_btn.connect("clicked", self.add_terminal)
        self.add_group_btn.connect("clicked", self.group_dialog)
        self.remove_group_btn.connect("clicked", self.remove_group)
        self.about_btn.connect("clicked", self.about_dialog)
        self.add_conn_btn.connect("clicked", self.connection_new)
        self.account_combobox.connect("changed", self.account_changed)
        self.conn_type_combobox.connect("changed", self.type_changed)
        self.name_property_value.connect("changed", self.connname_changed)
        self.user_property_value.connect("changed", self.username_changed)
        self.pass_property_value.connect("changed", self.password_changed)
        self.host_property_value.connect("changed", self.host_changed)
        self.port_property_value.connect("changed", self.port_changed)
        self.local_port_entry.connect("changed", self.local_port_changed)
        self.remote_port_entry.connect("changed", self.remote_port_changed)
        self.ssh_args_entry.connect("changed", self.arguments_changed)
        self.commands_entry.connect("changed", self.commands_changed)
        self.remove_conn_btn.connect("clicked", self.remove_connection_clicked)
        self.select_all_conn_btn.connect("clicked", self.listbox_select_all, self.conn_listbox)
        self.remove_sel_file_folder_btn.connect("clicked", self.remove_file_folder_clicked)
        self.add_file_btn.connect("clicked", self.add_file_folder_clicked, False)
        self.add_folder_btn.connect("clicked", self.add_file_folder_clicked, True)
        self.ssh_accounts_btn.connect("clicked", self.account_dialog)

    def config_widgets(self):
        self.add_terminal_btn.hide()
        self.conn_listbox.set_header_func(self.add_separators, None)
        self.group_prop_listview.set_header_func(self.add_separators, None)
        self.conn_prop_listview.set_header_func(self.add_separators, None)
        self.conn_files_listview.set_header_func(self.add_separators, None)
        self.group_desc_textview.set_buffer(self.group_desc_buffer)
        self.group_desc_buffer.set_text("Description")
        self.group_desc_textview.set_editable(True)

    def msg_dialog(self, head, body):
        msg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                    Gtk.ButtonsType.OK, head)
        msg.format_secondary_text(body)
        msg.run()
        msg.destroy()

    def add_separators(self, row, before, user_data):
        if before and not row.get_header():
            row.set_header(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

    def account_dialog(self, button):
        dialog = AccountWindow(self, queries.get_account(None))
        response = dialog.run()
        dialog.destroy()

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
                self.msg_dialog("Could not create group!",  "An error occurred when creating group '" + name + "'")

        dialog.destroy()
        self.clear_listbox(self.group_listbox)
        self.load_groups()

    def group_title_changed(self, entry):
        row = self.group_listbox.get_selected_row()
        try:
            new_name = entry.get_text()
            if new_name == '':
                now = datetime.now()
                new_name = 'Unknown ' + now.strftime("%d/%m/%Y %H:%M:%S")
            queries.change_group(row.group_id,
                                 {'name': new_name})
            row.label.set_label(new_name)
        except Exception as e:
            print(e)

    def group_desc_changed(self, buffer):
        row = self.group_listbox.get_selected_row()
        try:
            new_desc = buffer.get_text(buffer.get_start_iter(),
                                       buffer.get_end_iter(),
                                       include_hidden_chars=True)
            queries.change_group(row.group_id,
                                 {'desc': new_desc})
            row.desc = new_desc
        except Exception as e:
            print(e)

    def account_changed(self, combobox):
        sel_id = combobox.get_active_id()
        if sel_id == 'custom':
            self.user_property_row.show()
            self.pass_property_row.show()
        else:
            account = queries.get_account(sel_id)[0]
            row = self.conn_listbox.get_selected_row()
            queries.change_connection(row.conn_id,
                                      {'username': account.name,
                                      'password': account.password})
            self.user_property_row.hide()
            self.pass_property_row.hide()

    def type_changed(self, combobox):
        if combobox.get_active_id() == '1':
            self.port_forwarding_frame.show()
        elif combobox.get_active_id() == '2':
            self.port_forwarding_frame.hide()
            self.conn_files_box.show()
            self.conn_files_frame.show()
        else:
            self.port_forwarding_frame.hide()
            self.conn_files_box.hide()
            self.conn_files_frame.hide()
        row = self.conn_listbox.get_selected_row()
        queries.change_connection(row.conn_id,
                                  {'session_type': combobox.get_active_id()})

    def connname_changed(self, entry):
        row = self.conn_listbox.get_selected_row()
        new_name = entry.get_text()
        if new_name == '':
            now = datetime.now()
            new_name = 'Unknown ' + now.strftime("%d/%m/%Y %H:%M:%S")
        queries.change_connection(row.conn_id,
                                  {'name': new_name})

    def username_changed(self, entry):
        row = self.conn_listbox.get_selected_row()
        new_user = entry.get_text()
        if new_user == '':
            new_user = 'Unknown'
        queries.change_connection(row.conn_id,
                                  {'username': new_user})
    def password_changed(self, entry):
        row = self.conn_listbox.get_selected_row()
        queries.change_connection(row.conn_id,
                                  {'password': entry.get_text()})

    def host_changed(self, entry):
        row = self.conn_listbox.get_selected_row()
        queries.change_connection(row.conn_id,
                                  {'host': entry.get_text()})

    def port_changed(self, entry):
        row = self.conn_listbox.get_selected_row()
        new_port = entry.get_text()
        try:
            new_port = int(new_port)
            queries.change_connection(row.conn_id,
                                      {'port': new_port})
        except:
            self.msg_dialog("Wrong port!",  "Port must be a number from 0 to 65535.")

    def password_changed(self, entry):
        row = self.conn_listbox.get_selected_row()
        queries.change_connection(row.conn_id,
                                  {'password': entry.get_text()})

    def local_port_changed(self, entry):
        row = self.conn_listbox.get_selected_row()
        new_port = entry.get_text()
        try:
            if new_port != '':
                new_port = int(new_port)
            else:
                new_port = None
            queries.change_connection(row.conn_id,
                                      {'forward_local': new_port})
        except:
            self.msg_dialog("Wrong port!",  "Port must be a number from 0 to 65535.")

    def remote_port_changed(self, entry):
        row = self.conn_listbox.get_selected_row()
        new_port = entry.get_text()
        try:
            if new_port != '':
                new_port = int(new_port)
            else:
                new_port = None
            queries.change_connection(row.conn_id,
                                      {'forward_remote': new_port})
        except:
            self.msg_dialog("Wrong port!",  "Port must be a number from 0 to 65535.")

    def arguments_changed(self, entry):
        row = self.conn_listbox.get_selected_row()
        queries.change_connection(row.conn_id,
                                  {'arguments': entry.get_text()})

    def commands_changed(self, entry):
        row = self.conn_listbox.get_selected_row()
        queries.change_connection(row.conn_id,
                                  {'commands': entry.get_text()})

    def listbox_select_all(self, button, listbox):
        listbox.select_all()

    def connection_new(self, button):
        group = self.group_listbox.get_selected_row().group_id
        now = datetime.now()
        timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
        queries.add_connection("New connection " + timestamp,
                               "192.168.0.1",
                               22,
                               "unknown",
                               '',
                               group,
                               0)
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

    def load_accounts_combo(self, user):
        self.account_combobox.get_model().clear()
        self.account_combobox.append("custom", "Custom")
        accounts = queries.get_account(None)
        active_item = "custom"
        for account in accounts:
            if account.name == user:
                active_item = str(account.id)
            self.account_combobox.append(str(account.id), account.name)
        self.account_combobox.set_active_id(active_item)

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
        tab.button.connect("clicked", self.tab_close_clicked, tab)
        self.terminals.append_page_menu(terminal, tab, Gtk.Label("Local"))
        self.terminals.show_all()

    def add_connection_clicked(self, button):
        self.add_conn_dialog.show_all()

    def cancel_new_conn_btn_clicked(self, button):
        self.add_conn_dialog.hide()

    def remove_connection_clicked(self, button):
        rows = self.conn_listbox.get_selected_rows()
        group = self.group_listbox.get_selected_row().group_id
        for row in rows:
            queries.delete_connection(row.conn_id)
        self.clear_listbox(self.conn_listbox)
        self.load_connections(group)

    def add_file_folder_clicked(self, button, folder):
        if folder:
            action = Gtk.FileChooserAction.SELECT_FOLDER
            title = "Please choose a folder"
        else:
            title = "Please choose a file"
            action = Gtk.FileChooserAction.OPEN
        dialog = Gtk.FileChooserDialog(title,
                                       self,
                                       action,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(600, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_folder = dialog.get_filename()
            conn_id = self.conn_listbox.get_selected_row().conn_id
            queries.add_file_folder_connection(conn_id, file_folder)
            self.load_files_folders(conn_id)

        dialog.destroy()

    def remove_file_folder_clicked(self, button):
        conn_id = self.conn_listbox.get_selected_row().conn_id
        row = self.conn_files_listview.get_selected_row()
        queries.delete_file_folder(row.ff_id)
        self.conn_files_listview.remove(row)

    def tab_close_clicked(self, button, tab):
        pagenum = self.terminals.page_num(tab)
        self.terminals.remove_page(pagenum)

    def search_btn_clicked(self, button):
        if self.search_revealer.get_reveal_child():
            self.search_revealer.set_reveal_child(False)
        else:
            self.search_revealer.set_reveal_child(True)

    def theme_change(self, button):
        settings = Gtk.Settings.get_default()
        if settings.get_property("gtk-application-prefer-dark-theme"):
            settings.set_property("gtk-application-prefer-dark-theme", False)
            button.set_property("text", "Dark theme")
        else:
            settings.set_property("gtk-application-prefer-dark-theme", True)
            button.set_property("text", "Light theme")

    def back_btn_clicked(self, button):
        if self.group_stack.get_visible_child_name() == "conn_details":
            self.group_stack.set_visible_child_name("group_details")
            if not self.mobile_view:
                button.hide()
        else:
            if self.mobile_view:
                self.left_view_stack.set_visible_child_name("groups_list")
                self.left_view_headerbar.show()
                self.right_view_headerbar.hide()

    def group_selected(self, widget, row):
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

    def load_files_folders(self, cid):
        self.clear_listbox(self.conn_files_listview)
        file_folders = queries.get_file_folder(None, cid)
        for ff in file_folders:
            row = FileFolderListRow(ff.source, ff.id)
            self.conn_files_listview.add(row)
        self.conn_files_listview.show_all()

    def connection_selected(self, widget, row):
        self.group_stack.set_visible_child_name("conn_details")
        self.back_btn.show()
        if self.mobile_view:
            self.left_view_headerbar.hide()
            self.headerbar_separator.hide()
            self.right_view_headerbar.show()

        connection = queries.get_connection(row.conn_id, None)[0]
        self.name_property_value.set_text(connection.name)
        self.user_property_value.set_text(connection.user)
        self.pass_property_value.set_text(connection.password)
        self.host_property_value.set_text(connection.host)
        self.port_property_value.set_text(str(connection.port))
        if connection.forward_local is not None:
            self.local_port_entry.set_text(str(connection.forward_local))
        if connection.forward_remote is not None:
            self.remote_port_entry.set_text(str(connection.forward_remote))
        self.load_accounts_combo(connection.user)

        self.conn_type_combobox.get_model().clear()
        types = queries.get_session_type(None)
        for t in types:
            self.conn_type_combobox.append(str(t.id), t.name)
        self.conn_type_combobox.set_active_id(str(connection.session_type.id))

        self.load_files_folders(connection.id)

        self.ssh_args_entry.set_text(connection.arguments)
        self.commands_entry.set_text(connection.commands)

    def stack_change(self, stack, param):
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

    def size_allocate(self, *args):
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
