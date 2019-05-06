project('sshorganizer',         version: '0.2.6',
  meson_version: '>= 0.48.0',
)

i18n = import('i18n')


subdir('data')
subdir('src')
subdir('po')

meson.add_install_script('build-aux/meson/postinstall.py')
