# group.py
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
from .custom_widgets import AccountListRow
from .queries import get_account, delete_account, change_account

@Gtk.Template(resource_path='/org/gnome/SSHOrganizer/modules/accounts.ui')
class AccountWindow(Gtk.Dialog):
    __gtype_name__ = 'AccountDialog'

    main_box = Gtk.Template.Child()
    name_entry = Gtk.Template.Child()
    pass_entry = Gtk.Template.Child()
    accounts_listbox = Gtk.Template.Child()
    edit_mode = False
    edit_id = None

    def __init__(self, parent, accounts):
        super().__init__(title="New account",
                         transient_for=parent,
                         modal=True,
                         destroy_with_parent=True,
                         use_header_bar = True)
        self.add_buttons("Cancel", Gtk.ResponseType.CANCEL,
                         "Add", Gtk.ResponseType.OK)
        content_area = self.get_content_area()
        content_area.pack_start(self.main_box, True, True, 0)
        self.set_default_size(420, 380)
        self.load_accounts(accounts)
        self.config_widgets()

    def config_widgets(self):
        self.ok_button = self.get_children()[1].get_children()[1].get_style_context()
        self.ok_button.add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        self.pass_entry.connect('icon-press', self.password_visibility)

    def load_accounts(self, accounts):
        for account in accounts:
            row = AccountListRow(account.name, account.password, account.id)
            row.button_edit.connect("clicked", self.account_edit, row)
            row.button_remove.connect("clicked", self.account_remove, row)
            self.accounts_listbox.add(row)
        self.accounts_listbox.show_all()

    def account_edit(self, button, row):
        self.get_children()[1].get_children()[1].set_label("Save")
        self.edit_mode = True
        self.edit_id = row.account_id
        self.name_entry.set_text(row.label.get_text())
        self.pass_entry.set_text(row.password)
        self.accounts_listbox.hide()

    def account_remove(self, button, row):
        delete_account(row.account_id)
        self.accounts_listbox.remove(row)

    def password_visibility(self, entry, icon, event):
        entry.set_visibility(not entry.get_visibility())
