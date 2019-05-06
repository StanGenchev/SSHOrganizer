pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
maindir = join_paths(pkgdatadir, 'sshorganizer')
moduledir = join_paths(maindir, 'extra_modules')
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
  'gi_composites.py',
  'main.py',
  'window.py',
]

sshorganizer_module_sources = [
  'extra_modules/__init__.py',
  'extra_modules/connection_listrow.py',
  'extra_modules/group_listrow.py',
]

install_data(sshorganizer_main_sources, install_dir: maindir)
install_data(sshorganizer_module_sources, install_dir: moduledir)
