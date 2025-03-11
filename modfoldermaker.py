from os import scandir, rename, makedirs, getcwd, system
from os.path import abspath, relpath, basename, join, isdir, isfile, dirname
from sys import argv
from shutil import copyfile
modcontent = []
if len(argv) > 1:
    modcontent = argv[1:]
else:
    modcontent = [f.name for f in scandir(getcwd()) if (not f.name.endswith(".py") and isfile(f))]
exports, modpath = abspath(getcwd()).split("Exports")

makedirs((modfolder:=join(getcwd(),"Mod", modpath)), exist_ok = True)

for modfile in modcontent:
    copyfile(abspath(modfile), dest:=join(getcwd(),modfolder, modfile))
    print(dest)
