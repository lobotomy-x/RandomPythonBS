#generates ply pointclouds from 3dmigoto framedumps, e.g. download gi-model-import-assets repo and set path to characters folder

import os, re, sys
import collections
from glob import glob
from os import chdir, getcwd, scandir, rename
from os.path import join, exists, isdir,dirname,basename
from pathlib import Path

from pathlib import Path
import time

def SearchFilesByExt(path):
    st = time.time()
    files = []
    valid = []
    for _ext in ('*.txt','*.fmt'):
        files.extend(glob(join(path,_ext)))
    for file in files:
        print(file)
        if exists(file) and not file.lower() in valid:
            valid.append(file.lower())
    return valid

def SearchFolder(path):
    txts = SearchFilesByExt(path)
    regex = r"(?:POSITION\: )((\-)?\d\.\d{6})\W ((\-)?\d\.\d{6})\W ((\-)?\d\.\d{6}\n)"
    subst = "\\g<1> \\g<3> \\g<5>\n"
    for txt in txts:
        print(txt)
        with open(txt, "r") as file:
            matches = re.findall(r"(?=POSITION:\W)(.+)\n", file.read())
            positions = []
            if(len(matches) < 1): continue
            for match in matches:
                position = re.sub(regex,subst, str(match) , count=0, flags= re.IGNORECASE | re.MULTILINE)
                posxyz = position.replace("POSITION: ","")
                posx,posy,posz = posxyz.split(", ")
                positions.append(f"{posx} {posy} {posz}\n")
            with open(os.path.join(os.path.dirname(txt), os.path.basename(txt) + "_verts.ply"), "w") as f:
                vertex_count = len(positions)
                header = f"ply\nformat ascii 1.0\nelement vertex {vertex_count}\nproperty double x\nproperty double y\nproperty double z\nend_header\n"
                f.write(header)
                f.writelines(positions)
                f.close()

for f in os.scandir(input("enter path with all the character folders")):
    if os.path.isdir(f.path) and os.path.exists(f.path):
        try:
            SearchFolder(f.path)
        except Exception as e:
            pass


#in progress obj version
#import os, re, sys
# import collections
# from glob import glob
# from os import chdir, getcwd, scandir, rename
# from os.path import join, exists, isdir,dirname,basename
# from pathlib import Path
# 
# from pathlib import Path
# import time
# 
# def SearchFilesByExt(path):
#     st = time.time()
#     files = []
#     valid = []
#     for _ext in ('*.txt','*.fmt'):
#         files.extend(glob(join(path,_ext)))
#     for file in files:
#         print(file)
#         if exists(file) and not file.lower() in valid:
#             valid.append(file.lower())
#     return valid
# 
# def SearchFolder(path):
#     txts = SearchFilesByExt(path)
#     # Define regex patterns for each data type
#     regex_position = r"(?:POSITION\: )((\-)?\d\.\d{6})\W ((\-)?\d\.\d{6})\W ((\-)?\d\.\d{6}\n)"
#     subst_position = "v \\g \\g \\g\n"
#     regex_texcoord = r"(?:TEXCOORD\: )((\-)?\d\.\d{6})\W ((\-)?\d\.\d{6}\n)"
#     subst_texcoord = "vt \\g \\g\n"
#     regex_normal = r"(?:NORMAL\: )((\-)?\d\.\d{6})\W ((\-)?\d\.\d{6})\W ((\-)?\d\.\d{6}\n)"
#     subst_normal = "vn \\g \\g \\g\n"
#     # ... add more regex patterns for other data types like COLOR, TANGENT, etc.
# 
#     for txt in txts:
#         print(txt)
#         with open(txt, "r") as file:
#             # Read all lines that start with a data type keyword
#             matches = re.findall(r"(?=(?:POSITION|TEXCOORD|NORMAL|COLOR|TANGENT|BLENDWEIGHT|BLENDINDICES):\W)(.+)\n", file.read())
#             positions = []
#             normals = []
#             texcoords = []
#             faces = []
#             # ... lists for other data types
# 
#             if(len(matches) < 1): continue
#             for match in matches:
#                 # Extract position data
#                 position = re.sub(regex_position,subst_position, str(match) , count=0, flags= re.IGNORECASE | re.MULTILINE)
#                 posxyz = position.replace("POSITION: ","v ")
#                 posx,posy,posz = posxyz.split(", ")
#                 positions.append(f"{posx} {posy} {posz}\n")
#                 # Extract texcoord data
#                 # Extract normal data
#                 normal = re.sub(regex_normal,subst_normal, str(match) , count=0, flags= re.IGNORECASE | re.MULTILINE)
#                 normalxyz = normal.replace("NORMAL: ","vn ")
#                 normalx,normaly,normalz = normalxyz.split(", ")
#                 normals.append(f"{normalx} {normaly} {normalz}\n")
#                 # ... extract other data types
#                 texcoord = re.sub(regex_texcoord,subst_texcoord, str(match) , count=0, flags= re.IGNORECASE | re.MULTILINE)
#                 texcoordxy = texcoord.replace("TEXCOORD: ","vt ")
#                 texcoordx,texcoordy = texcoordxy.split(", ")
#                 texcoords.append(f"{texcoordx} {texcoordy}\n")
#                 face = f"{posx}/{texcoordx}"
# 
#             with open(os.path.join(os.path.dirname(txt), os.path.basename(os.path.dirname(txt)) + "_vertsnew.ply"), "a") as f:
#                 vertex_count = len(positions)
#                 # Include properties for all extracted data types in the header
#                 #header = f"ply\nformat ascii 1.0\nelement vertex {vertex_count}\nproperty double x\nproperty double y\nproperty double z\nproperty double u\nproperty double v\nproperty double nx\nproperty double ny\nproperty double nz\nend_header\n" # ... add other properties
#               #  f.write(header)
#                 # Write data for each vertex, combining all extracted data types
#                 for i in range(vertex_count):
#                     f.write(positions[i])
#                     f.write(texcoords[i])
#                     f.write(normals[i])
#                     # ... write other data types
#                 f.close()
# 
# for f in os.scandir(input("enter path with all the character folders")):
#     if os.path.isdir(f.path) and os.path.exists(f.path):
#         try:
#             SearchFolder(f.path)
#         except Exception as e:
#             pass
