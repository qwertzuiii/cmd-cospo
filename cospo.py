import os
import importlib
import bin.plugins.gpkg_reader as gpkg
import json

if os.path.exists('bin/project.gpkg'):
    if os.path.exists('bin/version.gpkg'):
        itsRootIThink = True
    else:
        itsRootIThink = False
else:
    itsRootIThink = False

if itsRootIThink:
    gpkg_project = open('bin/project.gpkg', 'rb').read()
    gpkg_project = gpkg.read(gpkg_project)
    gpkg_project = json.loads(gpkg_project)
    gpkg_version = open('bin/version.gpkg', 'rb').read()
    gpkg_version = gpkg.read(gpkg_version)
    gpkg_version = json.loads(gpkg_version)


def startHeader():
    if itsRootIThink:
        print(' {}, by {} - version {} ({})'.format(gpkg_project['project_name'].upper(), gpkg_project['project_creator'], gpkg_version['version'], gpkg_version['buildnum']))
    else:
        print(' CMD-COSPO, by qwertzuiii - version / (/)')
    print()
    print()

class errors:
    def not_enough_arguments():
        print('Not enough Arguments!')
    
    def module_not_found(module_name=""):
        print(f'Module "{module_name}" not found/installed!')

    def attribute_error(module_name=""):
        print(f'run() cannot be found in module "{module_name}"!')

class cmdlist:
    def help():
        print('HEKL')
        pass

    def runcode(ARGV):
        if len(ARGV) < 2:
            return errors.not_enough_arguments()

        if os.path.exists('bin/plugins/'+ARGV[1]+'.py'):
            x = 'bin.plugins.'+ARGV[1]
        else:
            x = ARGV[1]

        print(x, ARGV[1])
        
        try:
            lib = importlib.import_module(x)
        except ModuleNotFoundError:
            return errors.module_not_found(ARGV[1])
        
        try:
            lib.run()
        except AttributeError:
            return errors.attribute_error(ARGV[1])


commands = {
    ":help": cmdlist.help,
    ":run": cmdlist.runcode
}

cwd = os.getcwd()
prompt_prefix = 'cospo @ {} $ '.format(cwd)

startHeader()

while True:


    i = input(prompt_prefix)

    c = i.split(' ')
    #print(c)

    if c[0] in commands:
        commands[c[0]](c)
    else:
        os.system(i)
