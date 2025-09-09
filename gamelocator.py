# game locator
from os.path import *
from os import system, chdir, environ, scandir, remove, makedirs
import win32com.client as win32
import ctypes


def contains(str1,str2):
    return str1.find(str2) > 0

def is_unity(path):
    if isdir(path) and path.contains("_Data") and isfile(path.split("_Data")[0]+".exe") or isfile(join(dirname(path), "GameAssembly.dll")) or isfile(join(dirname(path), "UnityPlayer.dll")) or "StreamingAssets" in path:
        return True
    return False

def is_ue_basedir(path):
    if isfile(join(path, "Manifest_NonUFSFiles_Win64.txt")) or isfile(join(path, "Manifest_UFSFiles_Win64.txt")): return True
    if isdir(join(path, "Engine")): return True
    return False




def wildcard_subdir(path, pattern = "Binaries\\Win64"):
    entries = [f.path for f in scandir(path) if isdir(f.path) and not is_unity(f.path)]
    if len(entries) == 0: return None
    for entry in entries:
        if isdir(goal:=join(entry, pattern)) and not entry.contains("Engine"):
            return goal
        elif is_ue_basedir(entry):
            _entries = [f.path for f in scandir(entry) if isfile(f.path) and f.name != "Engine"]
            if len(_entries) > 0:
                for i in range(0, len(_entries)-1):
                    if isdir(goal:=join(entry, _entries[i], pattern)):
                        return goal
        wcs = [f.path for f in scandir(entry) if isdir(f.path) and f.name not in ["Content","Saved","Config","Plugins"] and not is_unity(f.path)]
        print(wcs)
        for wc in wcs:
            if isdir(goal2:=join(wc, pattern)):
                return goal2
            elif len([file.path for file in scandir(wc) if isdir(file.path)]) > 0:
                print("WOW didnt think we'd get here")
        else: return None


def ResolveShortcut(path):
    shell = win32.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    return shortcut.TargetPath

def get_game_paths():
    paths = []
    drives = []
    for _ord in range(65, 90):
        try:
            steam = "Program Files (x86)\\Steam" if _ord == 67 else "SteamLibrary"
            if isdir(steamlib:=join(f"{chr(_ord)}:\\", steam, "steamapps","Common")):
                print(steamlib)
                for f in scandir(steamlib):
                    if isdir(f.path) and wildcard_subdir(f.path) is not None:
                        paths.append(wc:=wildcard_subdir(f.path))
            if isdir(games:=join(chr(_ord), "Games")):
                for f in scandir(games):
                    print(f.path)
                    if isdir(f.path) and wildcard_subdir(f.path) is not None:
                        paths.append(wc:=wildcard_subdir(f.path))
                        print(wc)
        except Exception as e: pass
    programData = join(environ["PROGRAMDATA"],"Microsoft\\Windows\\Start Menu\\Programs")
    lnks = [dirname(ResolveShortcut(file.path)) for file in scandir(programData) if file.name.endswith(".lnk") and dirname(ResolveShortcut(file.path)).endswith("Win64") ]
    lnkdirs = [f.path for f in scandir(programData) if isdir(f.path)]
    for lnkdir in lnkdirs:
        lnks.extend([dirname(ResolveShortcut(file.path)) for file in scandir(lnkdir) if file.name.endswith(".lnk") and dirname(ResolveShortcut(file.path)).endswith("Win64") ])
    paths.extend([lnk for lnk in lnks if not lnk in paths])
    dirs = [
        join(f.path, "Saved", "Crashes")
        for f in scandir(environ["LOCALAPPDATA"])
        if isdir(join(f.path, "Saved", "Crashes"))
    ]
    dirs.extend(
        [
            join(f.path, "Saved", "Crashes")
            for f in scandir(environ["LOCALAPPDATA"])
            if isdir(join(f.path, "Steam", "Saved", "Crashes"))
        ]
    )
    try:
        for _dir in dirs:
            files = [
                join(f.path, "CrashContext.runtime-xml")
                for f in scandir(_dir)
                if isdir(f.path)
            ]
            if len(files) > 0:
                if len(files) > 1:
                    files.sort(key=getmtime)
                latest = files[-1]
                with open(latest, "r") as f:
                    for line in f.readlines():
                        try:
                            basedir = line.split("BaseDir")[1]
                            if basedir is not None:
                                if (win64 := basedir.find("Win64")) != -1:
                                    basedir = basedir[1:win64] + "Win64"
                                    #print(basedir)
                                    if isdir(basedir):
                                        paths.append(basedir)
                                        break
                        except Exception as e:
                            continue
    except Exception as e : pass
        
    return paths


get_game_paths()
