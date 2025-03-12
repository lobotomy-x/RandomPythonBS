from os.path import join, dirname, basename, isdir, isfile, relpath, abspath, getctime, getsize
from os import rename, getcwd, system, scandir, chdir, makedirs, symlink, remove
from datetime import datetime
from sys import argv
from tempfile import gettempdir



# trash cleanup script to manage some of blender's absurd bloat from autosaves
safe_mode = True
date_regex = r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}_)'
removal_folder = join(gettempdir(), 'blend_cleanup')
if not isdir(removal_folder):
    makedirs(removal_folder)

def unneeded_autosave(path):
    if path.endswith(("Unnamed.blend1","autosave.blend")) and (getctime(path) < datetime.now().timestamp() - 86400):
        return True
    return False

def safe_copy(src, dest = removal_folder):
    # rename is the preferred way to move files in python but it can't handle cross drive moves
    # so shutil is usually recommended, except it falls apart with anything non-ascii
    # most python users including package writers stop here
    # we could invoke system to use robocopy but that would be kind of bitch made
    # the answer is honestly really obvious and if this stumped you I think you need to learn a lower level language
    # legit just read the bytes and immediately write them at the intended destination or store it with mmap if you want to do anything to it
    data = open(src, "r+b").read()
    with open(join(dest, basename(src)), "wb") as f:
        f.write(data)
        f.seek(0)
        f.close()


def ascii_letters(string):
    # these numbers simply correspond to lowercase a-z and thus we have an easy oneliner to get only letters
    return ''.join(x for x in string if (97 <= ord(x) <= 122))



search_paths = [getcwd(), dirname(__file__), gettempdir()]
if len(argv) > 1:
    search_paths.extend(argpaths:=[path for path in argv[1:] if isdir(path)])
    if len(argv) -1 > len(argpaths):
        for arg in argv:
            if arg.endswith(("del", "remove","unsafe", "rem", "delete")):
                safe_mode = False

for _dir in search_paths:
    with open(join(dirname(__file__), "cleanup_log.txt"), "w") as logfile:
        for entry in scandir(_dir):
            try:
                if isdir(entry.path) or dirname(entry.path) == removal_folder:
                    continue
                if not isfile(entry.path):
                    continue
                if unneeded_autosave(entry.path):
                    if safe_mode:
                        safe_copy(entry.path)
                        logfile.write(f"Moved {entry.name} to {removal_folder}\n")
                    remove(entry.path)
                    logfile.write(f"Removed {entry.name}\n")
                elif entry.name.endswith((".blend1")):

                        if isfile(og:=entry.name.rsplit("1")[0]) or unneeded_autosave(entry.path):
                            if safe_mode:
                                safe_copy(entry.path)
                                logfile.write(f"Moved {entry.name} to {removal_folder}\n")
                            remove(entry.path)
                            logfile.write(f"Removed {entry.name}\n")
                elif entry.name.endswith(".blend"):

                    similar_key = ascii_letters(str(entry.name).lower())
                    print(similar_key)
                    similar_files = [f.path for f in scandir(_dir) if ascii_letters(str(f.name).lower()).startswith(similar_key)]
                    latest_similar = entry.path
                    latest_ctime = getctime(entry.path)
                    if len(similar_files) > 1:
                        for f in similar_files:
                            if getctime(f) > latest_ctime:
                                latest_ctime = getctime(f)
                                latest_similar = f
                    if latest_similar != entry.path and getctime(entry.path) < datetime.now().timestamp() - 86400:
                        if safe_mode:
                            safe_copy(entry.path)
                            logfile.write(f"Moved {entry.name} to {removal_folder}\n")
                        remove(entry.path)
                        logfile.write(f"Removed {entry.name}\n")
            except:
                    pass

print("Done scanning.")
size = 0
if safe_mode:
    print("Found and collected the following files:\n")
    files = [f.path for f in scandir(removal_folder) if isfile(f.path)]
    for f in files:
        print(f)
    print("Ensure that nothing has been collected by mistake.\n")
    if input("Delete files (y/n)") == "y":
        for f in files:
            size += getsize(f)
            remove(f)
    size_mb = size / (1024 * 1024)
    print(f"Reclaimed {size_mb} MB")
