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

@Gtk.Template(resource_path='/org/gnome/SSHOrganizer/modules/group.ui')
class GroupWindow(Gtk.Dialog):
    __gtype_name__ = 'GroupDialog'

    main_box = Gtk.Template.Child()
    name_entry = Gtk.Template.Child()
    desc = Gtk.Template.Child()

    def __init__(self, parent):
        super().__init__(title="New group",
                         transient_for=parent,
                         modal=True,
                         destroy_with_parent=True,
                         use_header_bar = True)
        self.add_buttons("Cancel", Gtk.ResponseType.CANCEL,
                         "Add", Gtk.ResponseType.OK)
        content_area = self.get_content_area()
        content_area.pack_start(self.main_box, True, True, 0)
        self.set_default_size(420, 240)
