#!/usr/bin/python3

import os, sys
import gi
import base64

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk

directory = os.getenv("HOME") + "/.multiconnections"
connections_file = directory + "/connections.list"
settings_file = directory + "/settings.conf"

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
    file.write("byobu\nTrue\nFalse")
    file.close()

class MultiConnections:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/opt/multiconnections/multiconnections.glade")
        self.builder.connect_signals(self)

        self.now_editing = 0
        self.continue_after_command = ";bash -l"
        self.continue_after_command_bool = 'True'
        self.default_command = 'byobu'

        self.store = Gtk.ListStore(str, str, str, str)

        self.listview = self.builder.get_object("listview1")
        self.listview.set_model(self.store)
        self.listview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)

        self.lang = os.getenv('LANG')
        if 'bg_BG' in self.lang:
            self.builder.get_object("toolbutton4").set_label("Премахване на всички")
            self.builder.get_object("toolbutton5").set_label("Свързване към всички")
            self.builder.get_object("label7").set_text("Изпълни следните команди след ssh:\nРаздели различните команди с ';'")
            self.builder.get_object("checkbutton4").set_label("Изпълни следните команди след ssh:\nРаздели различните команди с ';'")
            self.builder.get_object("checkbutton1").set_label("Покажи паролата")
            self.builder.get_object("checkbutton2").set_label("Изчисти при добавяне")
            self.builder.get_object("checkbutton3").set_label("Покажи паролата")
            self.builder.get_object("dialog3").set_title("Настройки")
            self.builder.get_object("dialog1").set_title("Добавяне на нова връзка")
            self.builder.get_object("dialog2").set_title("Редактиране на връзка")
            self.builder.get_object("label1").set_text("Потребител:")
            self.builder.get_object("label2").set_text("Адрес:")
            self.builder.get_object("label3").set_text("Парола:")
            self.builder.get_object("label9").set_text("Команда/и:")
            self.builder.get_object("label4").set_text("Потребител:")
            self.builder.get_object("label5").set_text("Адрес:")
            self.builder.get_object("label6").set_text("Парола:")
            self.builder.get_object("label8").set_text("Команда/и:")
            self.column = Gtk.TreeViewColumn("Потребител, адрес, парола и команда/и.")
        else:
            self.column = Gtk.TreeViewColumn("Username, address, password and command/s.")

        username = Gtk.CellRendererText()
        address = Gtk.CellRendererText()
        password = Gtk.CellRendererText()
        com = Gtk.CellRendererText()

        self.column.pack_start(username, True)
        self.column.pack_start(address, True)
        self.column.pack_start(password, True)
        self.column.pack_start(com, True)

        self.column.add_attribute(username, "text", 0)
        self.column.add_attribute(address, "text", 1)
        self.column.add_attribute(password, "text", 2)
        self.column.add_attribute(com, "text", 3)

        self.listview.append_column(self.column)

        self.window = self.builder.get_object("window1")
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

        self.get_connections()
        self.load_settings()

        self.window.show_all()

    def state_event(self, widget, event):
        if event.changed_mask & Gdk.WindowState.MAXIMIZED:
            if self.window.is_maximized() != True:
                self.wstate = "True"
                file = open(settings_file, "w")
                file.write(self.default_command + '\n' + self.continue_after_command_bool + '\nTrue')
                file.close()
            else:
                self.wstate = "False"
                file = open(settings_file, "w")
                file.write(self.default_command + '\n' + self.continue_after_command_bool + '\nFalse')
                file.close()

    def load_settings(self):
        with open(settings_file) as f:
            lines = f.readlines()
        self.default_command = lines[0].replace('\n','')
        self.builder.get_object("entry7").set_text(self.default_command)
        self.builder.get_object("entry9").set_text(self.default_command)
        self.continue_after_command_bool = lines[1].replace('\n','')
        self.wstate = lines[2].replace('\n','')
        if self.continue_after_command_bool == "True":
            self.builder.get_object("checkbutton4").set_active(True)
        else:
            self.builder.get_object("checkbutton4").set_active(False)
        if self.wstate == "True":
            self.window.maximize()

    def get_connections(self):
        with open(connections_file) as f:
            lines = f.readlines()
        for i in lines:
            if i == "\n":
                break
            i = i.replace('\n','').split('<mc>')
            self.store.append([i[0],i[1],i[2],i[3]])

    def save_connections(self):
        all_connections = ''
        model = self.listview.get_model()
        for item in model:
            all_connections += item[0] + "<mc>" + item[1] + "<mc>" + item[2] + "<mc>" + item[3] + '\n'
        with open(connections_file, "w") as c:
            c.write(all_connections)

    def connect(self, button):
        command_all = 'gnome-terminal'
        selection = self.listview.get_selection()
        model, pathlist = selection.get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            passwd = str(base64.b64decode(model.get_value(tree_iter,2)))
            passwd = passwd[2:]
            passwd = passwd[:-1]
            if self.continue_after_command_bool == 'True':
                command_all += ' --tab -e "bash -c \\"' + "sshpass -p '" + passwd + "' ssh -o StrictHostKeyChecking=no " + model.get_value(tree_iter,0) + "@" + model.get_value(tree_iter,1) + " -t '" + model.get_value(tree_iter,3) + self.continue_after_command + "';" + '\\""'
            else:
                command_all += ' --tab -e "bash -c \\"' + "sshpass -p '" + passwd + "' ssh -o StrictHostKeyChecking=no " + model.get_value(tree_iter,0) + "@" + model.get_value(tree_iter,1) + " -t '" + model.get_value(tree_iter,3) + "';" + '\\""'
        if command_all != 'gnome-terminal':
            os.system(command_all)

    def connect_to_all(self, button):
        command_all = 'gnome-terminal'
        model = self.listview.get_model()
        for item in model:
            passwd = str(base64.b64decode(item[2]))
            passwd = passwd[2:]
            passwd = passwd[:-1]
            if self.continue_after_command_bool == 'True':
                command_all += ' --tab -e "bash -c \\"' + "sshpass -p '" + passwd + "' ssh -o StrictHostKeyChecking=no " + item[0] + "@" + item[1] + " -t '" + item[3] + self.continue_after_command + "';" + '\\""'
            else:
                command_all += ' --tab -e "bash -c \\"' + "sshpass -p '" + passwd + "' ssh -o StrictHostKeyChecking=no " + item[0] + "@" + item[1] + " -t '" + item[3] + "';" + '\\""'
        if command_all != 'gnome-terminal':
            os.system(command_all)

    def check_for_duplicates(self, uname, addr, com):
        for item in self.store:
            if item[0] == uname and item[1] == addr and item[3] == com:
                return True
        return False

    def add_entry(self, button):
        self.builder.get_object("entry9").set_text(self.default_command)
        self.add_dialog.show_all()

    def add_new_entry(self, button):
        uname = self.builder.get_object("entry1").get_text()
        address = self.builder.get_object("entry2").get_text()
        com = self.builder.get_object("entry9").get_text()
        if self.check_for_duplicates(uname, address, com):
            if 'bg_BG' in self.lang:
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
                self.store.append([uname, address, passwd, com])

                self.save_connections()

                if self.builder.get_object("checkbutton2").get_active():
                    self.builder.get_object("entry1").set_text('')
                    self.builder.get_object("entry2").set_text('')
                    self.builder.get_object("entry3").set_text('')
                    self.builder.get_object("entry9").set_text(self.default_command)
            else:
                if 'bg_BG' in self.lang:
                    dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Има празно поле!")
                    dialog.format_secondary_text("Не може да има празно поле за потребител, адрес или парола.")
                else:
                    dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "You have a blank entry!")
                    dialog.format_secondary_text("You can`t have a blank entry for username, address or password.")
                dialog.run()
                dialog.destroy()

    def show_password_add(self, button):
        value = self.builder.get_object("checkbutton1").get_active()
        self.builder.get_object("entry3").set_visibility(value)

    def show_password_edit(self, button):
        value = self.builder.get_object("checkbutton3").get_active()
        self.builder.get_object("entry6").set_visibility(value)

    def add_cancel(self, button):
        self.add_dialog.hide()

    def remove_entry(self, button):
        selection = self.listview.get_selection()
        model, pathlist = selection.get_selected_rows()
        try:
            tree_iter = model.get_iter(pathlist[0])
            self.store.remove(tree_iter)
        except:
            pass
        self.save_connections()

    def delete_all(self, button):
        self.store.clear()
        self.save_connections()

    def edit_entry(self, button):
        selection = self.listview.get_selection()
        model, pathlist = selection.get_selected_rows()
        try:
            tree_iter = model.get_iter(pathlist[0])
            rownumobj = model.get_path(tree_iter)
            self.now_editing = int(rownumobj.to_string())
            self.builder.get_object("entry4").set_text(model.get_value(tree_iter,0))
            self.builder.get_object("entry5").set_text(model.get_value(tree_iter,1))
            passwd = str(base64.b64decode(model.get_value(tree_iter,2)))
            passwd = passwd[2:]
            passwd = passwd[:-1]
            self.builder.get_object("entry6").set_text(passwd)
            self.builder.get_object("entry8").set_text(model.get_value(tree_iter,3))
            self.edit_dialog.show_all()
        except:
            if 'bg_BG' in self.lang:
                dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Моля изберете връзка!")
            else:
                dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Please select a connection!")
            dialog.run()
            dialog.destroy()

    def edit_save(self, button):
        model = self.listview.get_model()
        model[self.now_editing][0] = self.builder.get_object("entry4").get_text()
        model[self.now_editing][1] = self.builder.get_object("entry5").get_text()
        passwd = str(base64.b64encode(str(self.builder.get_object("entry6").get_text()).encode("utf-8")))
        passwd = passwd[2:]
        passwd = passwd[:-1]
        model[self.now_editing][2] = passwd
        model[self.now_editing][3] = self.builder.get_object("entry8").get_text()
        self.edit_dialog.hide()
        self.save_connections()

    def edit_cancel(self, button):
        self.edit_dialog.hide()

    def settings(self, button):
        self.settings_dialog.show_all()

    def cancel_settings(self, button):
        self.settings_dialog.hide()

    def save_settings(self, button):
        self.default_command = self.builder.get_object("entry7").get_text()
        self.continue_after_command_bool = str(self.builder.get_object("checkbutton4").get_active())
        file = open(settings_file, "w")
        file.write(self.default_command + '\n' + self.continue_after_command_bool + '' + self.wstate)
        file.close()
        self.settings_dialog.hide()

    def destroy(self, window):
        Gtk.main_quit()


def main():
    app = MultiConnections()
    Gtk.main()

if __name__ == "__main__":
    main()

