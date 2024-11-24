from os.path import join, isfile, splitext, dirname
from json import load
from os import getcwd, rename, chdir, scandir


def GetJson(path):
    for f in scandir(path):
        if splitext(f.name)[1] == ".json":
            return f.name

def RenameKtoV(path):
    nd = dirname(path) if isfile(path) else path
    chdir(nd)
    if isfile(f:=GetJson(path)):
        namecfg = load(open(f, "r"))
        for k in namecfg:
            v = namecfg[k]
            if splitext(k)[1] == "":
                k += splitext(v)[1]
            elif splitext(v)[1] == "":
                k += splitext(k)[1]
            if isfile(join(getcwd(), v)):
                rename(v, k)

def RenameVtoK(path):
    nd = dirname(path) if isfile(path) else path
    chdir(nd)
    if isfile(f:=GetJson(path)):
        namecfg = load(open(f, "r"))
        for k in namecfg:
            v = namecfg[k]
            if splitext(k)[1] == "":
                k += splitext(v)[1]
            elif splitext(v)[1] == "":
                k += splitext(k)[1]
            if isfile(join(getcwd(), k)):
                rename(k, v)


RenameKtoV(getcwd())