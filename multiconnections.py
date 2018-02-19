#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gi, os, sys, base64

gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')

from gi.repository import Gtk, Gdk, Vte, GLib
from getpass import getuser

directory = os.getenv("HOME") + "/.multiconnections"
connections_file = directory + "/connections.list"
settings_file = directory + "/settings.conf"
session = os.environ.get('DESKTOP_SESSION')
#session = "test"
session_language = os.getenv('LANG')
#session_language = "test"

if not os.path.exists(directory):
    os.makedirs(directory)

try:
    os.stat(connections_file)
except:
    file = open(connections_file, "w")
    file.close()

try:
    os.stat(settings_file)
except:
    file = open(settings_file, "w")
    file.write("uname -a\nFalse")
    file.close()

class MultiConnections:
    def __init__(self):
        self.builder = Gtk.Builder()
        if "gnome" in session:
            try:
               self.builder.add_from_file("/opt/multiconnections/csd.glade")
               self.builder.add_from_file("/opt/multiconnections/csd-dialogs.glade")
            except:
               self.builder.add_from_file("csd.glade")
               self.builder.add_from_file("csd-dialogs.glade")
            self.builder.connect_signals(self)
            self.popup = self.builder.get_object("pop")
            self.menu_button = self.builder.get_object("menubutton")
            if 'bg_BG' in session_language:
                self.builder.get_object("dialog3title").set_text("Настройки")
                self.builder.get_object("dialog1title").set_text("Добавяне на нова връзка")
                self.builder.get_object("dialog2title").set_text("Редактиране на връзка")
        else:
            try:
               self.builder.add_from_file("/opt/multiconnections/noncsd.glade")
               self.builder.add_from_file("/opt/multiconnections/dialogs.glade")
            except:
               self.builder.add_from_file("noncsd.glade")
               self.builder.add_from_file("dialogs.glade")
            if 'bg_BG' in session_language:
                self.builder.get_object("dialog1").set_title("Добавяне на нова връзка")
                self.builder.get_object("dialog2").set_title("Редактиране на връзка")
                self.builder.get_object("dialog3").set_title("Настройки")
            self.builder.connect_signals(self)

        self.window = self.builder.get_object("multiconnections")
        self.listview = self.builder.get_object("listview")
        self.notebook = self.builder.get_object("notebook")
        self.close_tab = self.builder.get_object("closetab")
        self.close_all_tab = self.builder.get_object("closealltabs")
        self.add_button = self.builder.get_object("add")
        self.remove_button = self.builder.get_object("remove")
        self.edit_button = self.builder.get_object("edit")
        self.copy_button = self.builder.get_object("copy")
        self.paste_button = self.builder.get_object("paste")
        self.connect_button = self.builder.get_object("connect")
        self.connect_all_button = self.builder.get_object("connectall")

        self.now_editing = 0
        self.default_command = ''

        self.store = Gtk.ListStore(str, str, str, str, str)

        self.listview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)

        if 'bg_BG' in session_language:
            self.notebook.set_tab_label_text(self.notebook.get_nth_page(0), "Връзки")
            self.close_all_tab.set_label("Разкачване от всички")
            self.builder.get_object("connectall").set_label("Свързване с всички")
            self.builder.get_object("label7").set_text("Изпълни следните команди след ssh:\nРаздели различните команди с ';'")
            self.builder.get_object("checkbutton1").set_label("Покажи паролата")
            self.builder.get_object("checkbutton2").set_label("Изчисти при добавяне")
            self.builder.get_object("checkbutton3").set_label("Покажи паролата")
            self.builder.get_object("labeltab1").set_text("Заглавие на терминал:")
            self.builder.get_object("labeltab2").set_text("Заглавие на терминал:")
            self.builder.get_object("label1").set_text("Потребител:")
            self.builder.get_object("label2").set_text("Адрес:")
            self.builder.get_object("label3").set_text("Парола:")
            self.builder.get_object("label9").set_text("Команда/и:")
            self.builder.get_object("label4").set_text("Потребител:")
            self.builder.get_object("label5").set_text("Адрес:")
            self.builder.get_object("label6").set_text("Парола:")
            self.builder.get_object("label8").set_text("Команда/и:")
            for i, column_title in enumerate(["Заглавие на терминал", "Потребител", "Адрес", "Парола", "Команда/и"]):
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                column.set_expand(True)
                self.listview.append_column(column)
        else:
            for i, column_title in enumerate(["Terminal title", "Username", "Address", "Password", "Command/s"]):
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                column.set_expand(True)
                self.listview.append_column(column)

        screen = Gdk.Screen.get_default()
        monitors = screen.get_n_monitors()
        smallestX = screen.get_monitor_geometry(0).width
        smallestY = screen.get_monitor_geometry(0).height
        for n in range(1, monitors):
            if screen.get_monitor_geometry(n).width < smallestX and screen.get_monitor_geometry(n).height < smallestY:
                smallestX = screen.get_monitor_geometry(n).width
                smallestY = screen.get_monitor_geometry(n).height
        smallestX = smallestX / 100
        smallestY = smallestY / 100
        smallestX = smallestX * 80
        smallestY = smallestY * 80
        self.window.set_default_size(smallestX, smallestY)

        self.add_dialog = self.builder.get_object("dialog1")
        self.add_dialog.connect('delete-event', lambda w, e: w.hide() or True)
        self.add_dialog.set_transient_for(self.window)
        self.edit_dialog = self.builder.get_object("dialog2")
        self.edit_dialog.connect('delete-event', lambda w, e: w.hide() or True)
        self.edit_dialog.set_transient_for(self.window)
        self.settings_dialog = self.builder.get_object("dialog3")
        self.settings_dialog.connect('delete-event', lambda w, e: w.hide() or True)
        self.settings_dialog.set_transient_for(self.window)

        self.listview.set_model(self.store)

        self.close_tab.hide()
        self.close_all_tab.hide()
        self.copy_button.hide()
        self.paste_button.hide()

        self.load_settings()
        self.get_connections()

        self.window.show()

    def load_settings(self):
        with open(settings_file) as f:
            lines = f.readlines()
        self.default_command = lines[0].replace('\n','')
        self.builder.get_object("entry7").set_text(self.default_command)
        self.builder.get_object("entry9").set_text(self.default_command)
        self.wstate = lines[1].replace('\n','')
        if self.wstate == "True":
            self.window.maximize()

    def get_connections(self):
        with open(connections_file) as f:
            lines = f.readlines()
        for connection in lines:
            if connection == "\n":
                break
            connection = connection.replace('\n','').split('<mc>')
            self.store.append(list(connection))

    def add_terminal(self, button):
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
        self.notebook.append_page(terminal, Gtk.Label(getuser() + "@here"))
        self.notebook.show_all()

    def start_terminal(self, label, commands):
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
        self.notebook.append_page(terminal, Gtk.Label(label))
        for item in commands:
                command += item + '\n'
        terminal.feed_child(command, len(command))
        self.notebook.show_all()

    def disconnect(self, button):
        self.notebook.remove_page(self.notebook.get_current_page())
        self.refresh_main_buttons()

    def disconnect_from_all(self, button):
        pages = self.notebook.get_n_pages() - 1
        while pages > 0:
                self.notebook.remove_page(pages)
                pages -= 1
        self.refresh_main_buttons()

    def copy_terminal(self, button):
        page = self.notebook.get_current_page()
        vter = self.notebook.get_nth_page(page)
        try:
            vter.copy_clipboard()
        except:
            vter.copy_clipboard_format(Vte.Format(1))

    def paste_terminal(self, button):
        page = self.notebook.get_current_page()
        vter = self.notebook.get_nth_page(page)
        vter.paste_clipboard()

    def refresh_main_buttons(self):
        ctab = self.notebook.get_current_page()
        if ctab == 0:
            self.main_header_toolbar("connectionslist")
        else:
            self.main_header_toolbar("terminal")

    def main_header_toolbar(self, view):
        if view == "connectionslist":
            self.close_tab.hide()
            self.close_all_tab.hide()
            self.copy_button.hide()
            self.paste_button.hide()
            self.add_button.show()
            self.remove_button.show()
            self.edit_button.show()
            if "gnome" in session:
                self.menu_button.show()
            else:
                self.connect_button.show()
                self.connect_all_button.show()
        else:
            self.close_tab.show()
            self.close_all_tab.show()
            self.copy_button.show()
            self.paste_button.show()
            self.add_button.hide()
            self.remove_button.hide()
            self.edit_button.hide()
            if "gnome" in session:
                self.menu_button.hide()
            else:
                self.connect_button.hide()
                self.connect_all_button.hide()

    def tab_event(self, widget, event):
        if event.type == 7 :
            ctab = self.notebook.get_current_page()
            if ctab == 0:
                self.main_header_toolbar("connectionslist")
            else:
                self.main_header_toolbar("terminal")
        elif event.type == 9:
            ctab = self.notebook.get_current_page()
            if ctab == 0:
                self.main_header_toolbar("connectionslist")
            else:
                self.main_header_toolbar("terminal")
        else:
            pass

    def window_state_change(self, widget, event):
        if event.changed_mask & Gdk.WindowState.MAXIMIZED:
            if self.window.is_maximized() != True:
                if self.wstate != "True":
                    self.wstate = "True"
                    file = open(settings_file, "w")
                    file.write(self.default_command + '\n' + 'True')
                    file.close()
            else:
                if self.wstate != "False":
                    self.wstate = "False"
                    file = open(settings_file, "w")
                    file.write(self.default_command + '\n' + 'False')
                    file.close()

    def save_connections(self):
        all_connections = ''
        model = self.listview.get_model()
        for item in model:
            all_connections += item[0] + "<mc>" + item[1] + "<mc>" + item[2] + "<mc>" + item[3] + "<mc>" + item[4] + '\n'
        with open(connections_file, "w") as c:
            c.write(all_connections)

    def connect(self, button):
        if "gnome" in session:
            self.popup.hide()
        selection = self.listview.get_selection()
        model, pathlist = selection.get_selected_rows()
        for path in pathlist:
            commands = []
            tree_iter = model.get_iter(path)
            passwd = str(base64.b64decode(model.get_value(tree_iter,3)))
            passwd = passwd[2:]
            passwd = passwd[:-1]
            commands.append("sshpass -p '" + passwd + "' ssh -o StrictHostKeyChecking=no " + model.get_value(tree_iter,1) + "@" + model.get_value(tree_iter,2))
            command_list = model.get_value(tree_iter,4)
            command_list = command_list.split(';')
            for item in command_list:
                commands.append(item)
            self.start_terminal(model.get_value(tree_iter,0), commands)

    def connect_to_all(self, button):
        if "gnome" in session:
            self.popup.hide()
        model = self.listview.get_model()
        for item in model:
            commands = []
            passwd = str(base64.b64decode(item[3]))
            passwd = passwd[2:]
            passwd = passwd[:-1]
            commands.append("sshpass -p '" + passwd + "' ssh -o StrictHostKeyChecking=no " + item[1] + "@" + item[2])
            command_list = item[4]
            command_list = command_list.split(';')
            for sub_command in command_list:
                commands.append(sub_command)
            self.start_terminal(item[0], commands)

    def add_new_entry(self, button):
        terminal_name = self.builder.get_object("entry11").get_text()
        uname = self.builder.get_object("entry1").get_text()
        address = self.builder.get_object("entry2").get_text()
        com = self.builder.get_object("entry9").get_text()
        if self.check_for_duplicates(uname, address, com):
            if 'bg_BG' in session_language:
                dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Връзката вече съществува!")
                dialog.format_secondary_text("Вече има връзка със същият потребител, адрес и команда.")
            else:
                dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "This entry already exists!")
                dialog.format_secondary_text("You already have an entry with the same username, address and command.")
            dialog.run()
            dialog.destroy()
        else:
            passwd = self.builder.get_object("entry3").get_text()
            if uname != '' and uname != " " and address != '' and address != " " and passwd != '' and passwd != " ":
                passwd = str(base64.b64encode(passwd.encode("utf-8")))
                passwd = passwd[2:]
                passwd = passwd[:-1]
                self.store.append([terminal_name, uname, address, passwd, com])

                self.save_connections()

                if self.builder.get_object("checkbutton2").get_active():
                    self.builder.get_object("entry11").set_text('')
                    self.builder.get_object("entry1").set_text('')
                    self.builder.get_object("entry2").set_text('')
                    self.builder.get_object("entry3").set_text('')
                    self.builder.get_object("entry9").set_text(self.default_command)
            else:
                if 'bg_BG' in session_language:
                    dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Има празно поле!")
                    dialog.format_secondary_text("Не може да има празно поле за потребител, адрес или парола.")
                else:
                    dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "You have a blank entry!")
                    dialog.format_secondary_text("You can`t have a blank entry for username, address or password.")
                dialog.run()
                dialog.destroy()


    def edit_entry(self, button):
        selection = self.listview.get_selection()
        model, pathlist = selection.get_selected_rows()
        try:
            tree_iter = model.get_iter(pathlist[0])
            rownumobj = model.get_path(tree_iter)
            self.now_editing = int(rownumobj.to_string())
            self.builder.get_object("entry10").set_text(model.get_value(tree_iter,0))
            self.builder.get_object("entry4").set_text(model.get_value(tree_iter,1))
            self.builder.get_object("entry5").set_text(model.get_value(tree_iter,2))
            passwd = str(base64.b64decode(model.get_value(tree_iter,3)))
            passwd = passwd[2:]
            passwd = passwd[:-1]
            self.builder.get_object("entry6").set_text(passwd)
            self.builder.get_object("entry8").set_text(model.get_value(tree_iter,4))
            self.edit_dialog.show_all()
        except:
            if 'bg_BG' in session_language:
                dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Моля изберете връзка!")
            else:
                dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Please select a connection!")
            dialog.run()
            dialog.destroy()

    def check_for_duplicates(self, uname, addr, com):
        for item in self.store:
            if item[1] == uname and item[2] == addr and item[4] == com:
                return True
        return False

    def add_entry(self, button):
        self.add_dialog.show_all()

    def edit_save(self, button):
        model = self.listview.get_model()
        model[self.now_editing][0] = self.builder.get_object("entry10").get_text()
        model[self.now_editing][1] = self.builder.get_object("entry4").get_text()
        model[self.now_editing][2] = self.builder.get_object("entry5").get_text()
        passwd = str(base64.b64encode(str(self.builder.get_object("entry6").get_text()).encode("utf-8")))
        passwd = passwd[2:]
        passwd = passwd[:-1]
        model[self.now_editing][3] = passwd
        model[self.now_editing][4] = self.builder.get_object("entry8").get_text()
        self.edit_dialog.hide()
        self.save_connections()

    def remove_entry(self, button):
        selection = self.listview.get_selection()
        model, pathlist = selection.get_selected_rows()
        try:
            for path in pathlist:
                tree_iter = model.get_iter(pathlist[0])
                self.store.remove(tree_iter)
        except:
            pass
        self.save_connections()

    def show_password_add(self, button):
        value = self.builder.get_object("checkbutton1").get_active()
        self.builder.get_object("entry3").set_visibility(value)

    def show_password_edit(self, button):
        value = self.builder.get_object("checkbutton3").get_active()
        self.builder.get_object("entry6").set_visibility(value)

    def add_cancel(self, button):
        self.builder.get_object("entry11").set_text('')
        self.builder.get_object("entry1").set_text('')
        self.builder.get_object("entry2").set_text('')
        self.builder.get_object("entry3").set_text('')
        self.builder.get_object("entry9").set_text(self.default_command)
        self.add_dialog.hide()

    def edit_cancel(self, button):
        self.edit_dialog.hide()

    def settings(self, button):
        self.settings_dialog.show_all()

    def cancel_settings(self, button):
        self.settings_dialog.hide()

    def save_settings(self, button):
        self.default_command = self.builder.get_object("entry7").get_text()
        file = open(settings_file, "w")
        file.write(self.default_command + '\n' + self.wstate)
        file.close()
        self.settings_dialog.hide()

    def destroy(self, window):
        Gtk.main_quit()


def main():
    app = MultiConnections()
    Gtk.main()

if __name__ == "__main__":
    main()

