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

from gi.repository import Gtk
from .gi_composites import GtkTemplate

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))

@GtkTemplate(ui='/org/gnome/Sshorganizer/window.ui')
class SshorganizerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'SshorganizerWindow'

    accounts_button = GtkTemplate.Child()
    back_button = GtkTemplate.Child()
    add_terminal_button = GtkTemplate.Child()
    SshorganizerWindow = GtkTemplate.Child()
    connections_list_continer = GtkTemplate.Child()
    connection_info_scrollview = GtkTemplate.Child()
    connections_listbox = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.back_button.hide()
        self.add_terminal_button.hide()
        items = 'This is a sorted ListBox Fail'.split()

        for item in items:
            row = ListBoxRowWithData(item)
            row.connect("focus-in-event", self.on_connection_selected)
            self.connections_listbox.add(row)
        self.connections_listbox.show_all()

    def on_create_terminal_clicked(self, button):
        pass

    def on_accounts_button_clicked(self, button):
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

    def on_back_button_clicked(self, button):
        self.connections_listbox.show()
        self.connection_info_scrollview.hide()
        self.back_button.hide()
        self.accounts_button.show()

    def on_connection_selected(self, row, event):
        print('select - ', row.data)
        # self.connections_listbox.hide()
        # self.connection_info_scrollview.show()
        # self.back_button.show()
        # self.accounts_button.hide()

    def on_size_allocate(self, *args):
        width, _ = self.SshorganizerWindow.get_size()
        if width <= 600:
            self.connection_info_scrollview.hide()
        else:
            self.connection_info_scrollview.show()
