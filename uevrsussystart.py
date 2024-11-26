import os
import psutil
import pyinjector
import subprocess
import sys
from shutil import copyfile


#automatically retrieves uevr dlls from your path with no hassle and manages starting and stopping the frontend

#should suffice for most games without anticheat. for games with it there can be issues. I have a much more powerful loader in the works that just isnt ready for public release so for now throwing this out there

#if you need to get 3dmigoto into a uevr game just put it in uevr plugins folder and use this

#if starting from shortcut, bat, or cmd first arg is gamepath everything else is game args, otherwise use interactively

#can handle double quotes so you can right click a game file and use copy as path without havint to delete the quotes

#normally will inject openxr_loader but if you type "late" as an arg it will instead copy openxrloader into the gamedir after startup and you will have to manually click reinitialize runtime. This works and is needed for some games

dlls = []
init_dir = os.path.dirname(sys.argv[0])

try:
	for f in os.scandir(os.getcwd()):
		if f.name.endswith(".dll"):
			dlls.append(f.path)
			print(f"found dll {f.path}")
except Exception as e:
	print(e)

def cleanup_procs(name):
	try:
		procs = [psutil.Process(p) for p in psutil.pids()]
		for proc in procs:
			if proc.name().startswith(name):
				proc.kill()
	except Exception as e:
		print(e)
late = 0

gamePath = ""
_args = ""



if len(sys.argv) <= 1:
	print("start any game as a suspended process")
	print("enter game path: ")
	gamePath = input()
	if gamePath.startswith('"') and gamePath.endswith('"'): gamePath = gamePath[1:-1]
	_args = input("enter startup args: ")
else:
	gamePath = sys.argv[1]
	_args = sys.argv[2:]



if "late" in _args:
	late = 1
	# split to list if its a string otherwise assume it was a list
	try:
		_args = _args.split()
	except Exception as e: pass
	_args.remove("late")


gameDir = os.path.dirname(gamePath)
gameName = os.path.basename(gamePath)
if os.path.isfile(game_oxr := os.path.join(gameDir, "openxr_loader.dll")):
	os.remove(game_oxr)
os.chdir(gameDir)
cleanup_procs(gameName)
game = subprocess.Popen(
	args=_args,
	executable=gameName,
	cwd=gameDir,
	shell=False,
	creationflags=4,
)
for dll in dlls:
	pyinjector.inject(game.pid, dll)
if len(dlls) == 0:
	#if input("inject") == "uevr":
	oxr =  os.path.join(os.environ['APPDATA'], "UnrealVRMod", "UEVR", "openxr_loader.dll")
	uevr = os.path.join(os.environ['APPDATA'], "UnrealVRMod", "UEVR-nightly", "UEVRBackend.dll")
	uevrnull = os.path.join(os.environ['APPDATA'], "UnrealVRMod", "UEVR", "UEVRPluginNullifier.dll")
	uevr_front = os.path.join(os.environ['APPDATA'], "UnrealVRMod", "UEVR", "UEVRInjector.exe")
	if not os.path.exists(uevr): uevr = os.path.join(os.environ['APPDATA'], "UnrealVRMod", "UEVR", "UEVRBackend.dll")
	pyinjector.inject(game.pid, uevr)
	pyinjector.inject(game.pid, uevrnull)
	cleanup_procs("UEVRInjector")
	if late == 0:
		copyfile(oxr, game_oxr)
		pyinjector.inject(game.pid, oxr)
	subprocess.Popen(executable = uevr_front, args = f'--attach-exe="{gameName}"')
	psutil.Process(game.pid).resume()
	if late == 1:
		copyfile(oxr, game_oxr)



psutil.Process(game.pid).resume()
