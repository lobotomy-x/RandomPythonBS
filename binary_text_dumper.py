from os import scandir, rename, makedirs, getcwd, system
from os.path import join, isdir, isfile, dirname, splitext
from sys import argv
import binary2strings as b2s



def print_strings_tofile(path = None, filetype = None, interesting = True):
    spath = getcwd() if path is None else path
    files = []
    if filetype is not None:
        files = [f.path for f in scandir(spath) if f.path.lower().endswith(tuple([j.lower() for j in filetype]))]
    else:
        files = [f.path for f in scandir(spath)]
    for f in files:
        bindat = open(f, "rb").read()
        text = b2s.extract_all_strings(bindat, min_chars=4, only_interesting=interesting)
        with open(join(getcwd(), str(f).replace(splitext(f)[1],".txt")), "a", encoding="utf-8") as otxt:
            textout = ""
            for string in text:
                if string[1] == "UTF8":
                    print(string[0], file=otxt)

def search_strings(search_terms, path = None, filetype = None, interesting = True):
    spath = getcwd() if path is None else path
    files = []
    if filetype is not None:
        files = [f.path for f in scandir(spath) if f.path.lower().endswith(tuple([j.lower() for j in filetype]))]
    else:
        files = [f.path for f in scandir(spath)]
    for f in files:
        bindat = open(f, "rb").read()
        text = b2s.extract_all_strings(bindat, min_chars=4, only_interesting=interesting)
        for term in search_terms:
            if any([term in txt[0] for txt in text]):
                print(f"found {term} in {f}")

search_strings(["000000006FAAE290.dds",],filetype=(".nr"))