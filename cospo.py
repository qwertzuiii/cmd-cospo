import os
import runpy
import _ccmd.plugins.gpkg_reader as gpkg
import json
import tomllib

import ctypes # For building to .exe

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

tomlfile = open(SCRIPT_PATH + "/_ccmd/config.toml", 'r').read()
toml_cfg = tomllib.loads(tomlfile)
toml_c = toml_cfg['console']
toml_f = toml_cfg['font']

if toml_c["gpkg_files_needed"]:
    gpkg_project = open(SCRIPT_PATH + '/_ccmd/project.gpkg', 'rb').read()
    gpkg_project = gpkg.read(gpkg_project)
    gpkg_project = json.loads(gpkg_project)
    gpkg_version = open(SCRIPT_PATH + '/_ccmd/version.gpkg', 'rb').read()
    gpkg_version = gpkg.read(gpkg_version)
    gpkg_version = json.loads(gpkg_version)


def startHeader():
    if toml_c["gpkg_files_needed"]:
        print(' {}, by {} - version {} ({})'.format(gpkg_project['project_name'].upper(), gpkg_project['project_creator'], gpkg_version['version'], gpkg_version['buildnum']))
    else:
        print(' CMD-COSPO, by qwertzuiii - version / (/)')
    print()
    print()

class errors:
    def not_enough_arguments():
        print('* Not enough Arguments!')
    
    def module_not_found(module_name=""):
        print(f'* Module "{module_name}" not found/installed!')
    
    def module_importing_exception(e=""):
        print(f'* Error while importing module: {str(e)}')

    def attribute_error(module_name=""):
        print(f'* run() cannot be found in module "{module_name}"!')
    
    def dir_not_found():
        print("* Directory don't found!")

class cmdlist:
    def help(ARGV):
        print('/')
        pass

    def runcode(ARGV, func_name="run", func_arguments = None):
        if len(ARGV) < 2:
            return errors.not_enough_arguments()

        if os.path.exists(SCRIPT_PATH + '\\_ccmd\\plugins\\' + ARGV[1] + '.py'):
            x = SCRIPT_PATH + '\\_ccmd\\plugins\\' + ARGV[1] + '.py'
        else:
            x = ARGV[1]
        
        #print(x)

        #print(x, ARGV[1])
        
        #  OLD IMPORTING METHOD
        # try:
        #     lib = importlib.import_module(x)
        # except ModuleNotFoundError:
        #     return errors.module_not_found(ARGV[1])

        try:
            plugin = runpy.run_path(x)
        except FileNotFoundError:
            return errors.module_not_found(ARGV[1])
        except Exception as e:
            return errors.module_importing_exception(e)
        
        try:
            if func_arguments == None:
                plugin[func_name]()
            else:
                plugin[func_name](func_arguments)
        except AttributeError:
            return errors.attribute_error(ARGV[1])
        
    def cd(ARGV):
        current = os.getcwd()
        current_s = current.split("\\")
        length_current = len(current_s)
        #print(f'DEBUG: {current_s}, {length_current}')

        if len(ARGV) < 2:
            return errors.not_enough_arguments()

        if ARGV[1] == "-":
            new = ""
            for i in range(length_current -1): # "-1" means go one back
                #print(f'DEBUG: {i}')
                new += current_s[i] + "\\"
        else:
            new = os.path.abspath(ARGV[1])
        
        #print(f'DEBUG: {new}')
        
        try:
            os.chdir(new)
        except FileNotFoundError:
            return errors.dir_not_found()



commands = {
    ":help": cmdlist.help,
    ":run": cmdlist.runcode,
    ":goto": cmdlist.cd
}



def _refresh_prefix():
    cwd = os.getcwd()
    if toml_c['prompt_prefix'] == "DEFAULT":
        return 'cospo @ {} $ '.format(cwd)
    else:
        i = toml_c['prompt_prefix']
        return i.replace('%path', cwd)

if toml_f["change_font"]:
    cmdlist.runcode(['', 'console_fontchanging'], func_name="_FONT_CHANGE", func_arguments=toml_f["font_name"])

if toml_c["start_with_header"]:
    startHeader()

while True:


    i = input(_refresh_prefix())

    c = i.split(' ')
    #print(c)

    if c[0] in commands:
        commands[c[0]](c)
    else:
        os.system(i)
