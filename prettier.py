import subprocess
import platform
from sublime import Region, load_settings
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
options = []

# convert the sublime-settings into cli args
for setting in setting_keys:
    opt = settings.get(setting['key'], False)
    if opt:
        options.append(setting['option'])
        if not isinstance(opt, bool):
            options.append(str(opt))


def do_replace(edit, view, region, replacement):
    encoding = view.encoding() if view.encoding() != 'Undefined' else 'utf-8'
    view.replace(edit, region, replacement.decode(encoding))


def report_error(returncode, err=None):
    print('prettier failed with error code ' + str(returncode))
    if err:
        print(err)

# Calls prettier on the given region and replaces code
def prettify_code(edit, view, region):
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
        region = Region(0, self.view.size())
        prettify_code(edit, self.view, region)


# Run prettier on a selection in a file
class PrettierSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        command = ['prettier'] + options + ['--stdin']
        for region in self.view.sel():
            text = self.view.substr(region)
            prettify_code(edit, self.view, region)


# Prettier event listeners
class PrettierListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        # Run the prettier sublime command on save if autoformat is set to true
        autoformat = settings.get('autoformat')
        if autoformat == True:
            view.run_command('prettier')
