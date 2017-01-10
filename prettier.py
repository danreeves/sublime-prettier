from subprocess import check_output, CalledProcessError
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


class PrettierCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        options = []
        for setting in setting_keys:
            opt = settings.get(setting['key'], False)
            if opt:
                options.append(setting['option'])
                if not isinstance(opt, bool):
                    options.append(str(opt))

        view = self.view
        view_region = Region(0, view.size())
        file_path = view.file_name()
        file_encoding = view.encoding() if view.encoding() != 'Undefined' else 'utf-8'
        command = ['prettier'] + options + [file_path]
        try:
            prettier_output = check_output(command)
            view.replace(edit, view_region, prettier_output.decode(file_encoding))
        except CalledProcessError as e:
            print('prettier failed with ' + str(e.returncode))
            if e.output:
                print(e.output)
