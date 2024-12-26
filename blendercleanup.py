from os.path import join, dirname, basename, isdir, isfile, relpath, abspath, getctime
from os import rename, getcwd, system, scandir, chdir, makedirs, symlink
from datetime import datetime
import re
from sys import argv
from tempfile import gettempdir
from shutil import move

# trash cleanup script to manage some of blender's absurd bloat from antisaves



date_regex = r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}_)'
deletion_folder = join(gettempdir(), 'blend_cleanup')
if not isdir(deletion_folder):
    makedirs(deletion_folder)

search_paths = [getcwd(), dirname(__file__), gettempdir()]
if len(argv) > 1:
    for arg in argv:
        search_paths.append()

with open(join(dirname(__file__), "cleanup_log.txt"), "w") as logfile:
    _deletion_folder = deletion_folder
    for _dir in search_paths:
        if _dir[0] != "C":
            _deletion_folder = join(_dir, "temp")
            if not isdir(_deletion_folder):
                makedirs(_deletion_folder)
        for entry in scandir(_dir):
            # get blendX files
            if entry.name.endswith(".blend1"):
                try:
                     if isfile(og:=entry.name.rsplit("1")[0]):
                         rename(entry.path, join(deletion_folder, entry.name))
                         print(og)
                         logfile.write(f"Moved {entry.name} to {_deletion_folder}\n")
                except:
                    pass
            elif entry.name.endswith(".blend") and re.match(date_regex, entry.name, re.IGNORECASE | re.MULTILINE):
                og_file = re.sub(date_regex, '', entry.name, 0,  re.IGNORECASE | re.MULTILINE)
                if isfile(og_file) and (getctime(og_file) > getctime(entry.path) or getctime(entry.path) < datetime.now().timestamp() - 86400):
                    rename(entry.path, join(_deletion_folder, entry.name))
                    logfile.write(f"Moved {entry.name} to {_deletion_folder}\n")
        if _deletion_folder != deletion_folder:
            for f in scandir(_deletion_folder):
                if isdir(f): continue
                move(f.path, join(deletion_folder, f.name))
