pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
maindir = join_paths(pkgdatadir, 'sshorganizer')
databasedir = join_paths(maindir, 'database')
dialogsdir = join_paths(maindir, 'dialogs')
widgetsdir = join_paths(maindir, 'widgets')
terminaldir = join_paths(maindir, 'terminal')
uidir = join_paths(maindir, 'ui')
gnome = import('gnome')

gnome.compile_resources('sshorganizer',
  'sshorganizer.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python3 = import('python3')

conf = configuration_data()
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'sshorganizer.in',
  output: 'sshorganizer',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

sshorganizer_main_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

sshorganizer_database_sources = [
  'database/__init__.py',
  'database/models.py',
  'database/queries.py',
]

sshorganizer_dialogs_sources = [
  'dialogs/__init__.py',
  'dialogs/group.py',
  'dialogs/about.py',
  'dialogs/accounts.py',
]

sshorganizer_widgets_sources = [
  'widgets/__init__.py',
  'widgets/custom_widgets.py',
]

sshorganizer_terminal_sources = [
  'terminal/__init__.py',
  'terminal/terminal.py',
]

sshorganizer_ui_sources = [
  'ui/window.ui',
  'ui/accounts.ui',
  'ui/group.ui',
]

install_data(sshorganizer_main_sources, install_dir: maindir)
install_data(sshorganizer_database_sources, install_dir: databasedir)
install_data(sshorganizer_dialogs_sources, install_dir: dialogsdir)
install_data(sshorganizer_widgets_sources, install_dir: widgetsdir)
install_data(sshorganizer_terminal_sources, install_dir: terminaldir)
install_data(sshorganizer_ui_sources, install_dir: uidir)
