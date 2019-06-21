# connection.py
#
# Copyright 2019 Станислав Генчев
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

@Gtk.Template(resource_path='/org/gnome/SSHOrganizer/dialogs/connection.ui')
class ConnectionWindow(Gtk.Dialog):
    __gtype_name__ = 'ConnectionDialog'

    main_view = Gtk.Template.Child()
    name_entry = Gtk.Template.Child()
    host_entry = Gtk.Template.Child()
    port_entry = Gtk.Template.Child()
    account_combobox = Gtk.Template.Child()
    user_entry = Gtk.Template.Child()
    pass_entry = Gtk.Template.Child()
    conn_type_combobox = Gtk.Template.Child()
    local_port_entry = Gtk.Template.Child()
    remote_port_entry = Gtk.Template.Child()
    port_forwarding_frame = Gtk.Template.Child()
    file_folder_frame = Gtk.Template.Child()
    conn_files_listview = Gtk.Template.Child()

    def __init__(self, parent, accounts, session_types):
        super().__init__(title="New connection",
                         transient_for=parent,
                         modal=True,
                         destroy_with_parent=True,
                         use_header_bar = True)
        self.add_buttons("Cancel", Gtk.ResponseType.CANCEL,
                         "Add", Gtk.ResponseType.OK)
        content_area = self.get_content_area()
        content_area.pack_start(self.main_view, True, True, 0)
        self.set_default_size(420, 520)
        self.load_accounts(accounts)
        self.load_types(session_types)
        self.connect_signals()

    def load_accounts(self, accounts):
        self.account_combobox.append("custom", "Custom")
        for account in accounts:
            self.account_combobox.append(str(account.id), account.name)
        self.account_combobox.set_active(0)

    def load_types(self, session_types):
        for session in session_types:
            self.conn_type_combobox.append(str(session.id), session.name)
        self.conn_type_combobox.set_active(0)

    def connect_signals(self):
        self.account_combobox.connect("changed", self.account_changed)
        self.conn_type_combobox.connect("changed", self.type_changed)

    def account_changed(self, combobox):
        if combobox.get_active_id() == 'custom':
            self.user_entry.show()
            self.pass_entry.show()
        else:
            self.user_entry.set_text('')
            self.user_entry.hide()
            self.pass_entry.set_text('')
            self.pass_entry.hide()

    def type_changed(self, combobox):
        if combobox.get_active_id() == '1':
            self.port_forwarding_frame.show()
        else:
            self.port_forwarding_frame.hide()
