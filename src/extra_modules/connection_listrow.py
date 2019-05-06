#!/usr/bin/env python3
# connection_listrow.py
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
