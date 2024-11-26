import os
import psutil
import pyinjector
from PyQt5 import QtWidgets, QtGui, QtCore
import subprocess
import sys
from shutil import copyfile


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
	_args = _args.split()
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
		pyinjector.inject(game.pid, game_oxr)
	subprocess.Popen(executable = uevr_front, args = f'--attach-exe="{gamePath}"')
	psutil.Process(game.pid).resume()
	if late == 1:
		copyfile(oxr, game_oxr)



psutil.Process(game.pid).resume()
