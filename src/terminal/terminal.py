#!/usr/bin/env python3
# terminal.py
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

from os import environ
from gi.repository import Gtk, Vte, GLib

class TerminalBox(Vte.Terminal):
    __gtype_name__ = 'TerminalBox'

    def __init__(self,
                 parent,
                 is_ssh=False,
                 title="Local",
                 passwd="",
                 commands=None,
                 conn_id=None,
                 tab_close_func=None):
        super().__init__()
        self.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            environ['HOME'],
            ["/bin/sh"],
            [b"PS1=[\u@\h \W]\\$ "],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            )
        self.set_scrollback_lines(-1)
        self.__passwd = passwd + "\n"
        self.__title = title
        self.__parent = parent
        self.__monitor_output = True
        self.__conn_id = conn_id
        self.__tab_close_func = tab_close_func
        if is_ssh == True:
            self.connect("contents_changed", self.__contents_changed)
        if commands is not None:
            self.__term_send_text(commands)

    def __contents_changed(self, terminal):
        ret, attributes = terminal.get_text(None, None)
        if ret is not None and self.__monitor_output is not False:
            lines = []
            for line in ret.split("\n"):
                if line != "":
                    lines.append(line)
            if (len(lines) > 2 and "Broken pipe" in lines[len(lines) - 2]):
                self.__monitor_output = False
                self.__msg_dialog("Connection error!",
                                  self.__title + " has a broken pipe error.")
                self.__tab_close_func(None, self.__conn_id, terminal)
            elif (len(lines) > 2 and "Connection timed out" in lines[len(lines) - 2]):
                self.__monitor_output = False
                self.__msg_dialog("Timeout error!",
                                  "Connection to " + self.__title + " timed out.")
                self.__tab_close_func(None, self.__conn_id, terminal)
            elif (len(lines) > 2 and "refused" in lines[len(lines) - 2]):
                self.__monitor_output = False
                self.__msg_dialog("Permission error!",
                                  "Connection to " + self.__title + " refused.")
                self.__tab_close_func(None, self.__conn_id, terminal)
            elif (len(lines) > 2 and "No route to host" in lines[len(lines) - 2]):
                self.__monitor_output = False
                self.__msg_dialog("Connection error!",
                                  "No route to " + self.__title + ".")
                self.__tab_close_func(None, self.__conn_id, terminal)
            elif (len(lines) > 3 and "yes/no" in lines[len(lines) - 1]):
                self.__term_send_text(
                    self.__yesno_msg_dialog(lines[len(lines) - 3],
                                            lines[len(lines) - 2] + \
                                            "\nDo you still want to connect?"))
            elif(len(lines) > 0 and "password" in lines[len(lines) - 1]):
                self.__monitor_output = False
                self.__term_send_text(self.__passwd, True)

    def __check_output(self, terminal):
        ret, attributes = terminal.get_text(None, None)
        if ret is not None:
            lines = []
            for line in ret.split("\n"):
                if line != "":
                    lines.append(line)
            if (len(lines) > 2 and "Permission denied" in lines[len(lines) - 2]):
                terminal.disconnect_by_func(self.__check_output)
                self.__msg_dialog("Permission denied!", "Could not connect to " + self.__title + ".")
                self.__tab_close_func(None, self.__conn_id, terminal)
            elif (len(lines) >= 2 and "password" not in lines[len(lines) - 1]):
                terminal.disconnect_by_func(self.__check_output)

    def __term_send_text(self, text, is_password=False):
        self.feed_child(text.encode("utf-8"))
        if is_password is True:
            self.connect("contents_changed", self.__check_output)

    def __msg_dialog(self, head, body):
        msg = Gtk.MessageDialog(self.__parent,
                                0,
                                Gtk.MessageType.INFO,
                                Gtk.ButtonsType.OK,
                                head)
        msg.format_secondary_text(body)
        msg.run()
        msg.destroy()

    def __yesno_msg_dialog(self, head, body):
        dialog = Gtk.MessageDialog(self.__parent,
                                   0,
                                   Gtk.MessageType.WARNING,
                                   Gtk.ButtonsType.OK_CANCEL,
                                   head)
        dialog.format_secondary_text(body)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.destroy()
            return "yes\n"
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return "no\n"
