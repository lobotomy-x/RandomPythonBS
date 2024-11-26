# uevrsussystart 

automatically retrieves uevr dlls from your path with no hassle and manages starting and stopping the frontend

should suffice for most games without anticheat. for games with it there can be issues. I have a much more powerful loader in the works that just isnt ready for public release so for now throwing this out there

if you need to get 3dmigoto into a uevr game just put it in uevr plugins folder and use this

if starting from shortcut, bat, or cmd first arg is gamepath everything else is game args, otherwise use interactively

can handle double quotes so you can right click a game file and use copy as path without havint to delete the quotes

normally will inject openxr_loader but if you type "late" as an arg it will instead copy openxrloader into the gamedir after startup and you will have to manually click reinitialize runtime. This works and is needed for some games

# jsonrenamer 

grabs the first json it sees adjacent and renames keys to values or values to keys. not setup for users, you need to edit it to run the command you need. for scripters its obviously something you know how to do but just a small time saver util

# gettransparentimages

makes a folder and moves anything with alpha values to it but with some specific handling for 3dmigoto frame analysis 


# killsus

kill bad procs including other python procs interactively on cli

# steam.pyw/startsteam

needed for some bypasses


