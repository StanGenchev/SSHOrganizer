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

import os, sys

from gi.repository import Gtk, Vte, GLib
from .gi_composites import GtkTemplate

class ConnectionListRow(Gtk.ListBoxRow):
    def __init__(self, name):
        super(Gtk.ListBoxRow, self).__init__()
        self.name = name
        self.box = Gtk.Box().new(Gtk.Orientation.HORIZONTAL, 6)
        self.box.set_border_width(6)
        self.label = Gtk.Label(name, xalign=0)
        self.box.pack_start(self.label, True, True, 0)
        self.button = Gtk.Button()
        self.button.set_image(Gtk.Image.new_from_icon_name("media-playback-start-symbolic",
                                                           Gtk.IconSize.SMALL_TOOLBAR))
        self.button.set_relief(Gtk.ReliefStyle.NONE)
        self.box.pack_start(self.button, False, True, 0)
        self.add(self.box)

class GroupListRow(Gtk.ListBoxRow):
    def __init__(self, name):
        super(Gtk.ListBoxRow, self).__init__()
        self.box = Gtk.Box().new(Gtk.Orientation.VERTICAL, 0)
        self.label = Gtk.Label(xalign=0)
        self.label.set_markup("<b>" + name + "</b>")
        self.label.set_margin_left(6)
        self.label.set_margin_right(6)
        self.label.set_sensitive(False)
        self.box.pack_start(self.label, True, True, 5)
        self.box.pack_start(Gtk.Separator(), True, True, 0)
        self.add(self.box)
        self.set_selectable(False)
        self.set_activatable(False)

@GtkTemplate(ui='/org/gnome/Sshorganizer/window.ui')
class SshorganizerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'SshorganizerWindow'

    SshorganizerWindow = GtkTemplate.Child()

    terminals_container = GtkTemplate.Child()

    # headerbar widgets
    users_button = GtkTemplate.Child()
    back_button = GtkTemplate.Child()
    add_terminal_button = GtkTemplate.Child()

    # connections view widgets
    connections_list_continer = GtkTemplate.Child()
    connection_info_scrollview = GtkTemplate.Child()
    connections_listbox = GtkTemplate.Child()
    connection_info_stack = GtkTemplate.Child()
    connections_stack = GtkTemplate.Child()
    connections_pane = GtkTemplate.Child()
    conn_name_entry = GtkTemplate.Child()
    conn_group_combo = GtkTemplate.Child()
    host_entry = GtkTemplate.Child()
    port_entry = GtkTemplate.Child()
    conn_user_combo = GtkTemplate.Child()
    conn_user_entry = GtkTemplate.Child()
    conn_pass_entry = GtkTemplate.Child()

    # terminals view widgets



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        items = 'Mumble Chat.Quanterall Aeternity Wine-HRS'.split()

        self.connections_listbox.add(GroupListRow("Quanterall"))
        for item in items:
            row = ConnectionListRow(item)
            row.connect("focus-in-event", self.on_connection_selected)
            self.connections_listbox.add(row)
        self.connections_listbox.show_all()
        command = "clear\n"
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
        self.terminals_container.append_page(terminal, Gtk.Label("term"))
        self.terminals_container.show_all()

    def on_create_terminal_clicked(self, button):
        pass

    def on_users_button_clicked(self, button):
        pass

    def on_hamburger_menu_clicked(self, button):
        pass

    def on_searchbar_reveal(self, *args):
        pass

    def on_search_text_change(self, *args):
        pass

    def on_add_button_clicked(self, button):
        pass

    def on_remove_button_clicked(self, button):
        pass

    def on_search_button_clicked(self, button):
        pass

    def on_group_combo_change(self, button):
        pass

    def on_user_combo_change(self, button):
        print(self.conn_user_combo.get_selected())

    def on_dark_theme_toggled(self, button):
        if button.get_active():
            settings = Gtk.Settings.get_default()
            settings.set_property("gtk-application-prefer-dark-theme", True)
        else:
            settings = Gtk.Settings.get_default()
            settings.set_property("gtk-application-prefer-dark-theme", False)

    def on_back_button_clicked(self, button):
        if self.connection_info_scrollview.get_parent().get_name() == "GtkStack":
            self.connections_stack.set_visible_child(self.connections_list_continer)
            self.back_button.hide()
            self.users_button.show()

    def on_connection_selected(self, row, event):
        if self.connection_info_scrollview.get_parent().get_name() == "GtkStack":
            self.connections_stack.set_visible_child(self.connection_info_scrollview)
            self.back_button.show()
            self.users_button.hide()

    def on_size_allocate(self, *args):
        width, _ = self.SshorganizerWindow.get_size()
        if width <= 600:
            if self.connection_info_scrollview.get_parent().get_name() != "GtkStack":
                self.connection_info_scrollview.reparent(self.connections_stack)
        else:
            if self.connection_info_scrollview.get_parent().get_name() == "GtkStack":
                self.connection_info_scrollview.reparent(self.connections_pane) 
