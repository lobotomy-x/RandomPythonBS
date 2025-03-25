Scripts I deem useful enough to share but not enough to need a separate repo. These can be used freely and dont need credit for usage but you cannot include any code or write functionally identical code without credit. Don't expect any support, if you have an issue its probably better to open the file and fix it yourself or ask an AI for help.

CLIs that need startup args are cringe so almost everything here should work just by double clicking the script in explorer. If that doesnt work for you try to remove python from user/system path, remove winstore python, and get the 64 bit windows installer for python 3.12.x 

Many of these are reusable with some tweaking. I've been making use of the new windows powertoys feature "new++" which gives you a second new file menu when right clicking in windows explorer that can be populated with your own scripts that can be copied wherever and used without altering the original. Very handy here

# unicopy.py 
Solves a few issues that shouldnt be issues but somehow are present in every python package outside builtins. No idea of speed but you're using python so you already didn't care. 

# blendercleanup.py
Helps reclaim space from blender's horrible autosaves that are ultimately necessary to avoid data loss. Not recursive, doesnt search globally unless you launch from CLI or shortcut with desired search paths as args. Run it in any folder with lots of blender files and it will move the files to your temp dir and then prompt you to delete them which is needed to actually get the space back. You can use rem, remove, del, or delete as a startup arg to directly delete files and skip this step. In either case please check carefully and understand you are responsible for any cases of data loss. I've erred on the side of caution here and ignore recent files even if they meet other conditions for removal. I don't check for anything not using .blend or .blend1 extensions so if you want to keep an older backup around and guarantee safety you could name to blend2 

# binary_text_dumper.py
uses binary2strings pip package to quickly pull candidate ascii strings from any files with matching filetypes specified in the script. The package uses a lightweight ml engine to try to identify interesting non-gibberish strings but the main value here is speed and ease of use. There is also a function to search for a string or set of strings and print any files containing it. This script is one you likely need to open up and adjust the invokation to use. No code knowledge actually required beyond being able to call a function or change parameters

# locate_nr_mesh
uses same package along with a windows file picker to allow Ninja Rip users to interactively search a framedump for their target mesh files by selecting dumped texture files that match their target object, e.g. select face texture for the player character and find all the files with the character model present

# cvar_differ
for UEVR users. Run from any folder to generate adjacent files with a list of cvars or commands that appear in multiple games and their count, a list of cvars that can only be found in one game, and a combined json of all cvars and a list of their unique values. Games with unique cvars will get a file listing them in their profile folder. Not all usable commands are included, e.g. toggledebugcamera usually works if you can spawn a native console

# modfoldermaker
put next to unreal asset you want to modify. Recreates folder structure in root of the current drive

# jsonrenamer 
grabs the first json it sees adjacent and renames keys to values or values to keys. not setup for users, you need to edit it to run the command you need. for scripters its obviously something you know how to do but just a small time saver util

# gettransparentimages
makes a folder and moves anything with alpha values to it but with some specific handling for 3dmigoto frame analysis 

# killsus

kill bad procs including other python procs interactively on cli, must run as admin

# steam.pyw/startsteam

needed for some bypasses


