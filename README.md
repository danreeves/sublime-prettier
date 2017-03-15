[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)
___

# Prettier

This is a Sublime Text 3 plugin for the [prettier](https://github.com/jlongster/prettier) JavaScript formatter.

## Installation

You need `prettier` installed globally for this plugin to work. See the [installation instructions](https://github.com/jlongster/prettier#usage).

`npm install -g prettier`

### Recommended

Install via [Package Control](https://packagecontrol.io/) *coming soon*.

### Manually

1. Go to
    * (Mac OS/OS X): `~/Library/Application\ Support/Sublime\ Text\ 3/Packages/"`
    * (Windows): `C:\Users\[username]\AppData\Roaming\Sublime Text 3\Packages`

2. `git clone git@github.com:danreeves/sublime-prettier.git` or [download](https://github.com/danreeves/sublime-prettier/archive/master.zip) the zip and extract to that location.

## Usage

### Command Palette

<dl>
    <dt>Format the entire file:</dt>
    <dd><code>Prettier: Format this file</code></dd>
    <dt>Format the current selection(s):</dt>
    <dd><code>Prettier: Format this selection</code></dd>
</dl>

### Hotkeys

- Linux: <kbd>ctrl+alt+p</kbd>
- Windows: <kbd>ctrl+alt+p</kbd>
- OS X: <kbd>ctrl+alt+p</kbd>

You can add [custom key bindings](https://www.sublimetext.com/docs/3/settings.html) using the commands `prettier` and `prettier_selection`.

## Configuration

The plugin takes the same settings and the `prettier` tool. See the [`prettier` repo](https://github.com/jlongster/prettier/blob/master/src/options.js) or [this repo](https://github.com/danreeves/sublime-prettier/blob/master/Prettier.sublime-settings). You can configure them in Sublime at `Preferences > Package Settings > Prettier`.

You can turn on the auto formatting on save by setting `autoformat` to `true`.

For example:

```js
{
  // Turns on/off autoformatting on save
  "autoformat": true,

  // Only attempt to format files with extensions set there
  "extensions": ["js", "jsx"],

  // Fit code within this line limit
  "printWidth": 80,

  // Number of spaces it should use per tab
  "tabWidth": 2,

  // Use the flow parser instead of babylon
  "useFlowParser": false,

  // If true, will use single instead of double quotes
  "singleQuote": false,

  // Controls the printing of trailing commas wherever possible
  "trailingComma": false,

  // Controls the printing of spaces inside array and objects
  "bracketSpacing": true
}
```
