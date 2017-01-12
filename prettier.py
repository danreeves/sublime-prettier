from subprocess import Popen, check_output, CalledProcessError, PIPE
from sublime import Region, load_settings
import sublime_plugin

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


# Run prettier an a file
class PrettierCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        path = self.view.file_name()
        command = ['prettier'] + options + [path]
        region = Region(0, self.view.size())
        try:
            prettier_output = check_output(command)
            do_replace(edit, self.view, region, prettier_output)
        except CalledProcessError as e:
            report_error(e.returncode, e.output)


# Run prettier on a selection in a file
class PrettierSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        command = ['prettier'] + options + ['--stdin']
        for region in self.view.sel():
            text = self.view.substr(region)
            proc = Popen(command, stdin=PIPE, stderr=PIPE, stdout=PIPE)
            prettier_output, err = proc.communicate(str.encode(text))
            if err or proc.returncode != 0:
                report_error(proc.returncode, err)
            else:
                do_replace(edit, self.view, region, prettier_output)
