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

from gi import require_version
require_version('Vte', '2.91')
from gi.repository import Gtk, Gdk, Vte, GLib
from .gi_composites import GtkTemplate

class ConnectionListRow(Gtk.ListBoxRow):
    def __init__(self, name):
        super(Gtk.ListBoxRow, self).__init__()
        self.name = name
        self.set_size_request(-1, 48)
        self.box = Gtk.Box().new(Gtk.Orientation.HORIZONTAL, 6)
        self.box.set_border_width(6)
        self.group_icon = Gtk.Image.new_from_icon_name("network-server-symbolic",
                                                             Gtk.IconSize.SMALL_TOOLBAR)
        self.label = Gtk.Label(name, xalign=0)

        self.button_run = Gtk.Button()
        self.button_run.set_image(Gtk.Image.new_from_icon_name("media-playback-start-symbolic",
                                                           Gtk.IconSize.SMALL_TOOLBAR))
        self.button_run.set_relief(Gtk.ReliefStyle.NONE)
        self.box.pack_start(self.group_icon, False, True, 6)
        self.box.pack_start(self.label, True, True, 0)
        self.box.pack_start(self.button_run, False, True, 0)
        self.add(self.box)

class GroupListRow(Gtk.ListBoxRow):
    def __init__(self, name, group_id):
        super(Gtk.ListBoxRow, self).__init__()
        self.set_size_request(-1, 48)
        self.group_id = group_id
        self.demo_desk = """This is a demo description. It does not represent final the final product!"""
        self.box = Gtk.Box().new(Gtk.Orientation.HORIZONTAL, 6)
        self.box.set_border_width(6)
        self.group_icon = Gtk.Image.new_from_icon_name("network-workgroup-symbolic",
                                                             Gtk.IconSize.SMALL_TOOLBAR)
        self.label = Gtk.Label(name, xalign=0)

        self.enter_group_icon = Gtk.Image.new_from_icon_name("go-next-symbolic",
                                                             Gtk.IconSize.SMALL_TOOLBAR)
        self.box.pack_start(self.group_icon, False, True, 6)
        self.box.pack_start(self.label, True, True, 0)
        self.box.pack_start(self.enter_group_icon, False, True, 6)
        self.add(self.box)

@GtkTemplate(ui='/org/gnome/Sshorganizer/window.ui')
class SshorganizerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'SshorganizerWindow'

    SshorganizerWindow = GtkTemplate.Child()

    # window header widgets
    headerbar_hbox = GtkTemplate.Child()
    left_view_headerbar = GtkTemplate.Child()
    headerbar_separator = GtkTemplate.Child()
    right_view_headerbar = GtkTemplate.Child()
    details_back_button = GtkTemplate.Child()
    conn_back_button = GtkTemplate.Child()
    search_conn_button = GtkTemplate.Child()

    # window body widgets
    body_hbox = GtkTemplate.Child()
    body_separator = GtkTemplate.Child()

    # connections pane widgets
    left_view_stack = GtkTemplate.Child()
    search_revealer = GtkTemplate.Child()
    conn_vbox = GtkTemplate.Child()
    conn_stack = GtkTemplate.Child()
    group_list_scrollview = GtkTemplate.Child()
    conn_list_scrollview = GtkTemplate.Child()
    group_listbox = GtkTemplate.Child()
    conn_listbox = GtkTemplate.Child()
    conn_name_entry = GtkTemplate.Child()
    conn_group_combo = GtkTemplate.Child()
    host_entry = GtkTemplate.Child()
    port_entry = GtkTemplate.Child()
    conn_user_combo = GtkTemplate.Child()
    conn_user_entry = GtkTemplate.Child()
    conn_pass_entry = GtkTemplate.Child()

    # right view widgets
    right_view_scroll = GtkTemplate.Child()
    right_view_viewport = GtkTemplate.Child()
    right_view_stack = GtkTemplate.Child()
    group_name = GtkTemplate.Child()
    group_desc = GtkTemplate.Child()
    conn_details_scroll = GtkTemplate.Child()
    group_details_scroll = GtkTemplate.Child()
    user_property_value = GtkTemplate.Child()
    host_property_value = GtkTemplate.Child()
    port_property_value = GtkTemplate.Child()

    # terminals view widgets

    # dialogs and other windows
    add_conn_dialog = GtkTemplate.Child()

    mobile_view = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        GLib.set_application_name(_("SSHOrganizer"))
        Gtk.Application.__init__(self, application_id="org.gnome.Sshorganizer")
        self.init_template()
        items = 'Quanterall Aeternity Wine-HRS CollectionTech'.split()

        for i, item in enumerate(items):
            row = GroupListRow(item, i)
            self.group_listbox.add(row)
        self.group_listbox.unselect_all()
        self.group_listbox.connect("row-selected", self.on_group_selected)
        self.group_listbox.connect("button-press-event", self.on_group_activated)
        self.group_listbox.show_all()
        # command = "clear\n"
        # terminal = Vte.Terminal()
        # terminal.spawn_sync(
        #     Vte.PtyFlags.DEFAULT,
        #     os.environ['HOME'],
        #     ["/bin/bash"],
        #     [],
        #     GLib.SpawnFlags.DO_NOT_REAP_CHILD,
        #     None,
        #     None,
        #     )
        # self.terminals_container.append_page(terminal, Gtk.Label("term"))
        # self.terminals_container.show_all()

    def on_add_connection_clicked(self, button):
        self.add_conn_dialog.show_all()

    def on_cancel_new_conn_button_clicked(self, button):
        self.add_conn_dialog.hide()

    def on_remove_connection_clicked(self, button):
        pass

    def on_search_conn_button_clicked(self, button):
        if self.search_revealer.get_reveal_child():
            self.search_revealer.set_reveal_child(False)
        else:
            self.search_revealer.set_reveal_child(True)

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

    def on_details_back_button_clicked(self, button):
        self.left_view_stack.set_visible_child(self.conn_vbox)
        self.left_view_headerbar.show()
        self.right_view_headerbar.hide()

    def on_conn_back_button_clicked(self, button):
        self.conn_stack.set_visible_child(self.group_list_scrollview)
        self.right_view_stack.set_visible_child(self.group_details_scroll)
        self.conn_back_button.hide()
        self.search_conn_button.show()

    def on_group_selected(self, widget, row):
        self.group_name.set_text(row.label.get_text())
        self.group_desc.set_text(row.demo_desk)
        if self.mobile_view:
            self.left_view_headerbar.hide()
            self.right_view_headerbar.show()
            self.details_back_button.show()
            self.left_view_stack.set_visible_child(self.right_view_stack)

    def on_group_activated(self, widget, event):
        if event.type == Gdk.EventType._2BUTTON_PRESS:
            self.conn_back_button.show()
            self.search_conn_button.hide()
            for index in range(len(self.conn_listbox)-1, -1, -1):
                self.conn_listbox.remove(self.conn_listbox.get_row_at_index(index))
            items = 'First Second Third'.split()
            for item in items:
                row = ConnectionListRow(item)
                self.conn_listbox.add(row)
            self.conn_listbox.show_all()
            self.conn_stack.set_visible_child(self.conn_list_scrollview)

    def on_connection_selected(self, parent, child):
        self.right_view_stack.set_visible_child(self.conn_details_scroll)
        self.user_property_value.set_text(child.label.get_text())
        self.host_property_value.set_text("192.168.0.2")
        self.port_property_value.set_text("22")
        self.left_view_stack.set_visible_child(self.right_view_stack)
        if self.mobile_view:
            self.left_view_headerbar.hide()
            self.right_view_headerbar.show()
            self.details_back_button.show()

    def on_size_allocate(self, *args):
        width, _ = self.SshorganizerWindow.get_size()
        if width <= 720:
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
            if self.right_view_stack.get_parent().get_name() == "GtkStack":
                self.right_view_headerbar.show()
                self.headerbar_separator.show()
                self.left_view_headerbar.set_show_close_button(False)
                self.headerbar_hbox.set_homogeneous(False)
                self.right_view_stack.reparent(self.right_view_viewport)
                self.body_separator.show()
                self.right_view_scroll.show()
                self.body_hbox.set_homogeneous(False)
                self.mobile_view = False
