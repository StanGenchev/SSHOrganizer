#!/usr/bin/env python3
# custom_widgets.py
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

from gi.repository import Gtk

class AccountListRow(Gtk.ListBoxRow):
    def __init__(self, name: str, password: str, account_id: int = 0):
        super(Gtk.ListBoxRow, self).__init__()
        self.account_id = account_id
        self.name = name
        self.password = password
        self.set_size_request(-1, 54)
        self.box = Gtk.Box().new(Gtk.Orientation.HORIZONTAL, 6)
        self.box.set_border_width(6)
        self.box.set_valign(Gtk.Align.CENTER)
        self.account_icon = Gtk.Image.new_from_icon_name("user-info-symbolic",
                                                         Gtk.IconSize.SMALL_TOOLBAR)
        self.label = Gtk.Label(name, xalign=0)

        self.button_edit = Gtk.Button()
        self.button_remove = Gtk.Button()
        self.button_edit.set_image(Gtk.Image.new_from_icon_name("document-edit-symbolic",
                                                           Gtk.IconSize.SMALL_TOOLBAR))
        self.button_remove.set_image(Gtk.Image.new_from_icon_name("edit-delete-symbolic",
                                                           Gtk.IconSize.SMALL_TOOLBAR))
        self.button_edit.set_relief(Gtk.ReliefStyle.NONE)
        self.button_remove.set_relief(Gtk.ReliefStyle.NONE)
        self.box.pack_start(self.account_icon, False, True, 6)
        self.box.pack_start(self.label, True, True, 0)
        self.box.pack_start(self.button_edit, False, True, 0)
        self.box.pack_start(self.button_remove, False, True, 6)
        self.add(self.box)
        self.set_selectable(False)

class ConnectionListRow(Gtk.ListBoxRow):
    def __init__(self, name: str, conn_id: int = 0):
        super(Gtk.ListBoxRow, self).__init__()
        self.conn_id = conn_id
        self.name = name
        self.set_size_request(-1, 54)
        self.box = Gtk.Box().new(Gtk.Orientation.HORIZONTAL, 6)
        self.box.set_border_width(6)
        self.box.set_valign(Gtk.Align.CENTER)
        self.conn_icon = Gtk.Image.new_from_icon_name("network-server-symbolic",
                                                             Gtk.IconSize.SMALL_TOOLBAR)
        self.label = Gtk.Label(name, xalign=0)

        self.button_run = Gtk.Button()
        self.button_run.set_image(Gtk.Image.new_from_icon_name("media-playback-start-symbolic",
                                                           Gtk.IconSize.SMALL_TOOLBAR))
        self.button_run.set_relief(Gtk.ReliefStyle.NONE)
        self.box.pack_start(self.conn_icon, False, True, 6)
        self.box.pack_start(self.label, True, True, 0)
        self.box.pack_start(self.button_run, False, True, 6)
        self.add(self.box)
        self.set_selectable(True)

class GroupListRow(Gtk.ListBoxRow):
    def __init__(self, name: str, desc: str, group_id: int = 0):
        super(Gtk.ListBoxRow, self).__init__()
        self.set_size_request(-1, 48)
        self.group_id = group_id
        self.desc = desc
        self.box = Gtk.Box().new(Gtk.Orientation.HORIZONTAL, 6)
        self.box.set_border_width(6)
        self.group_icon = Gtk.Image.new_from_icon_name("network-workgroup-symbolic",
                                                       Gtk.IconSize.SMALL_TOOLBAR)
        self.label = Gtk.Label(name, xalign=0)
        self.box.pack_start(self.group_icon, False, True, 6)
        self.box.pack_start(self.label, True, True, 6)
        self.add(self.box)

class FileFolderListRow(Gtk.ListBoxRow):
    def __init__(self, source: str, ff_id: int = 0):
        super(Gtk.ListBoxRow, self).__init__()
        self.set_size_request(-1, 48)
        self.ff_id = ff_id
        self.label = Gtk.Label(source, xalign=0)
        self.label.set_margin_left(12)
        self.label.set_margin_right(12)
        self.add(self.label)
        self.set_selectable(True)

class TabWidget(Gtk.HBox):
    def __init__(self, name: str = "Local"):
        super(Gtk.HBox, self).__init__()
        self.button = Gtk.Button()
        image = Gtk.Image.new_from_icon_name("window-close-symbolic", Gtk.IconSize.MENU)
        self.button.set_image(image)
        self.button.set_relief(Gtk.ReliefStyle.NONE)
        label = Gtk.Label(name)
        self.pack_start(label, False, False, 0)
        self.pack_start(self.button, False, False, 0)
        self.set_spacing(6)
        self.show_all()
