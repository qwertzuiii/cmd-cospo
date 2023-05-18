#### [Download](https://github.com/qwertzuiii/cmd-cospo/releases/latest)

# cmd-cospo

A customizable cmd with plugins to install.

## Basic Commands
- `:run [PluginName (or path if not in plugins directory), no .py at the end!]` - Runs plugins
- `:goto -/[DirectoryName]` - Replaces the `cd` command (just type `-` to go a directory back)
- `:quit` - Replaces the `exit` command
- ... All other windows cmd commands

---

## TODOs

- [ ] Adding more commands
    - [ ] `:help` command
    - ...

---

## How to make plugins for cospo?
Just make a `.py` file in `_ccmd/plugins/` and make a `def run():` function

### Adding other libraries can cause problems! To add other libraries you need to edit the source code of cospo!
You need to import these libraries in `cospo.py` and compile it!

## How to edit the source code?

[Download source code](https://github.com/qwertzuiii/cmd-cospo/archive/refs/heads/main.zip)

`pip install -r requirements.txt`

## How to compile the source code?
- Download [`fast-py-builder-ui`](https://github.com/qwertzuiii/fast-py-builder-ui/releases)

- Edit `build.json` in `_build` and set the full paths

- Open the builder [Tip: You can use System Environments to put the builder in a Folder, to open it easily in a cmd!] and select the `build.json` and click on **Build**