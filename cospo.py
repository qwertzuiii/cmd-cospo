import os
import runpy
import ccmd.plugins.gpkg_reader as gpkg
import json
import tomllib

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

gpkg_project = open(SCRIPT_PATH + '/ccmd/project.gpkg', 'rb').read()
gpkg_project = gpkg.read(gpkg_project)
gpkg_project = json.loads(gpkg_project)
gpkg_version = open(SCRIPT_PATH + '/ccmd/version.gpkg', 'rb').read()
gpkg_version = gpkg.read(gpkg_version)
gpkg_version = json.loads(gpkg_version)

tomlfile = open(SCRIPT_PATH + "/ccmd/config.toml", 'r').read()
toml_cfg = tomllib.loads(tomlfile)
toml_c = toml_cfg['console']
toml_f = toml_cfg['font']

def startHeader():
    print(' {}, by {} - version {} ({})'.format(gpkg_project['project_name'].upper(), gpkg_project['project_creator'], gpkg_version['version'], gpkg_version['buildnum']))
    print()
    print()

class errors:
    def not_enough_arguments():
        print('Not enough Arguments!')
    
    def module_not_found(module_name=""):
        print(f'Module "{module_name}" not found/installed!')
    
    def module_importing_exception(e=""):
        print(f'Error while importing module: {str(e)}')

    def attribute_error(module_name=""):
        print(f'run() cannot be found in module "{module_name}"!')

class cmdlist:
    def help():
        print('HEKL')
        pass

    def runcode(ARGV, func_name="run", func_arguments = None):
        if len(ARGV) < 2:
            return errors.not_enough_arguments()

        if os.path.exists(SCRIPT_PATH + '\\ccmd\\plugins\\' + ARGV[1] + '.py'):
            x = SCRIPT_PATH + '\\ccmd\\plugins\\' + ARGV[1] + '.py'
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


commands = {
    ":help": cmdlist.help,
    ":run": cmdlist.runcode
}

cwd = os.getcwd()

if toml_c['prompt_prefix'] == "DEFAULT":
    prompt_prefix = 'cospo @ {} $ '.format(cwd)
else:
    prompt_prefix = toml_c['prompt_prefix']

if toml_f["change_font"]:
    cmdlist.runcode(['', 'console_fontchanging'], func_name="_FONT_CHANGE", func_arguments=toml_f["font_name"])

if toml_c["start_with_header"]:
    startHeader()

while True:


    i = input(prompt_prefix)

    c = i.split(' ')
    #print(c)

    if c[0] in commands:
        commands[c[0]](c)
    else:
        os.system(i)
