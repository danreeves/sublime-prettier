> [This was a quick prototype but there's another package on Package Control. Use that one instead](https://packagecontrol.io/packages/JsPrettier). Thanks 👋

---

# Prettier

This is a Sublime Text 3 plugin for the [prettier](https://github.com/jlongster/prettier) JavaScript formatter.

## Installation

You need `prettier` installed globally for this plugin to work. See the [installation instructions](https://github.com/jlongster/prettier#usage).

`npm install -g prettier`

### Recommended

Install via [Package Control](https://packagecontrol.io/) *coming soon*.

### Manually

1. Go to
    * (Mac OS/OS X): `cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/"`
    * (Windows): `C:\Users\[username]\AppData\Roaming\Sublime Text 3\Packages`

2. `git clone git@github.com:danreeves/sublime-prettier.git` or [download](https://github.com/danreeves/sublime-prettier/archive/master.zip) the zip and extract to that location.

## Usage

### Command Palette

Open the command palette and search for `Prettier: Auto format this file`

### Hotkeys

- Linux: <kbd>ctrl+alt+p</kbd>
- Windows: <kbd>ctrl+alt+p</kbd>
- OS X: <kbd>ctrl+alt+p</kbd>

## Configuration

The plugin takes the same settings and the `prettier` tool. See the [`prettier` repo](https://github.com/jlongster/prettier/blob/master/src/options.js) or [this repo](https://github.com/danreeves/sublime-prettier/blob/master/Prettier.sublime-settings). You can configure them in Sublime at `Preferences > Package Settings > Prettier`.
