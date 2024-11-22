from os import system, chdir, getcwd

if getcwd() != "C:\\Program Files (x86)\\Steam": chdir("C:\\Program Files (x86)\\Steam")
system("Set __COMPAT_LAYER=RUNASINVOKER")
system('Start "" steam.exe')
