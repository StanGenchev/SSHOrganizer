# about.py

copyright = "Copyright 2019 Станислав Генчев"
license = '''Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

The software is provided "As is", without warranty of any kind,
express or implied, including but not limited to the warranties of
merchantability, fitness for a particular purpose and
noninfringement. In no event shall the x consortium be liable for any
claim, damages or other liability, whether in an action of contract,
tort or otherwise, arising from, out of or in connection with the
software or the use or other dealings in the software.

Except as contained in this notice, the name(s) of the above copyright
holders shall not be used in advertising or otherwise to promote the sale,
use or other dealings in this Software without prior written
authorization.'''

from gi.repository import Gtk

class AboutWindow(Gtk.AboutDialog):
    __gtype_name__ = 'AboutDialog'

    def __init__(self, parent):
        super().__init__(title="About",
                         transient_for=parent,
                         modal=True,
                         destroy_with_parent=True,
                         use_header_bar=True)
        self.set_logo_icon_name("network-workgroup")
        self.set_program_name("SSHOrganizer")
        self.set_copyright(copyright)
        self.set_license(license)
        self.set_version('0.4.3')
        self.set_website("https://github.com/StanGenchev/SSHOrganizer")
        self.set_website_label("Source and documentation")
        self.set_default_size(440, 320)
