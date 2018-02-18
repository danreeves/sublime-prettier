import subprocess
import platform
import os
from sublime import Region, load_settings, expand_variables
import sublime_plugin

IS_WINDOWS = platform.system() == 'Windows'

setting_keys = [
    {'key': 'printWidth', 'option': '--print-width'},
    {'key': 'tabWidth', 'option': '--tab-width'},
    {'key': 'useFlowParser', 'option': '--flow-parser'},
    {'key': 'singleQuote', 'option': '--single-quote'},
    {'key': 'trailingComma', 'option': '--trailing-comma'},
    {'key': 'bracketSpacing', 'option': '--bracket-spacing'},
]
settings = load_settings('Prettier.sublime-settings')


def do_replace(edit, view, region, replacement):
    encoding = view.encoding() if view.encoding() != 'Undefined' else 'utf-8'
    view.replace(edit, region, replacement.decode(encoding))


def report_error(returncode, err=None):
    print('prettier failed with error code ' + str(returncode))
    if err:
        print(err)


def make_flag(setting):
    return '%s=%s' % (setting['option'], str(settings.get(setting['key'], False)).lower())


def find_config_path(file_name, variables):
    process = subprocess.Popen(['prettier', '--find-config-path', file_name],
                               stdout=subprocess.PIPE)
    output = process.communicate()[0]
    try:
        path = output.decode('utf-8').splitlines()[0]
    except IndexError:
        path = None
    if path:
        return path
    config_locations = settings.get('configLocations', [])
    for path in config_locations:
        path = expand_variables(path, variables)
        if os.path.isfile(path):
            return path
    return None


# Calls prettier on the given region and replaces code
def prettify_code(edit, view, config_file_name, region):
    if config_file_name:
        options = ['--config', config_file_name]
    else:
        options = [make_flag(setting) for setting in setting_keys]
    command = ['prettier'] + options + ['--stdin']
    code = view.substr(region)
    proc = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell=IS_WINDOWS
    )
    prettier_output, err = proc.communicate(str.encode(code))

    if err or proc.returncode != 0:
        report_error(proc.returncode, err)
    else:
        do_replace(edit, view, region, prettier_output)


# Run prettier an a file
class PrettierCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        extensions = settings.get('extensions')
        file_name = self.view.file_name()

        # Check if the file extension is allowed
        file_extension = os.path.splitext(file_name)[1][1:]
        if extensions and file_extension not in extensions:
            print('Prettier can\'t format .%s files' % file_extension)
            return

        variables = dict(self.view.window().extract_variables())
        variables.update({'home_path': os.path.expanduser('~')})
        config_file_name = find_config_path(file_name, variables) if file_name else None
        region = Region(0, self.view.size())
        prettify_code(edit, self.view, config_file_name, region)


# Run prettier on a selection in a file
class PrettierSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            prettify_code(edit, self.view, region)


# Prettier event listeners
class PrettierListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        # Run the prettier sublime command on save if autoformat is set to true
        autoformat = settings.get('autoformat')
        if autoformat is True:
            view.run_command('prettier')
