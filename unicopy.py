# Copyright Lobotomyx 2025 
# All usage rights granted, user assumes all liability, 
# credit should be given either by directly downloading this file and preserving the header,
# or with a simple mention or link to the repo. e.g. if you want to copy the text directly 
# you can just put a comment above the function linking here whatever it doesnt matter really
from os.path import join, dirname, basename
from os import makedirs



# easy file ops using only os and builtins
# works crossdrive, with any format, and any text encoding
def unicopy(src, dest, move = False):
    # this isn't really any better or worse than using 'with' context
    # but I kind of want to show that you don't need to follow convention
    # especially if that convention came from people who couldnt figure this out
    data = (file:=open(src, "r+b")).read()
    # you'd think not assigning the retval from 'open' would mean it closes right away but apparently not
    file.close()
    # check if extension is passed while allowing relative paths with '.\\'
    if str(dest).replace("/","\\").rfind("\\") > str(dest).rfind("."):
      dest = join(dest, basename(src))
    makedirs(dirname(dest), exist_ok = True)
    # if you want to do anything to the file you could import mmap and return the handle
    with open(dest, "wb") as f:
        f.write(data)
        f.seek(0)
        f.close()
    if move:
      if open(dest, "r+b").read() == data:
        from os import remove
        remove(src)


# throwing this in as a freebie
# if you need to preserve case then make sure to use a copy
def ascii_letters(string):
    # these numbers simply correspond to lowercase a-z and thus we have an easy oneliner to get only english letters
    return ''.join(x for x in string.lower() if (97 <= ord(x) <= 122))


# usage examples
# from os import scandir
# for f in scandir("H:\\Test\\这会破坏你的代\\files"):
#   unicopy(f.path, ".\\ntest", True)

# example use case for ascii_letters: matching materials and diffuse textures
# in reality you should just open the materials to find the texture name but whatever
# skips 'MI' prefix for mat and for texture replaces T and D
# def match_texture(mat, texture_paths):
#   for tex in texture_paths:
#     print(ascii_letters(basename(mat)[2:].rsplit(".")[0]))
#     print(ascii_letters(basename(tex)[1:].rsplit("D.")[0]))
#     if ascii_letters(basename(mat)[2:].rsplit(".")[0]) == ascii_letters(basename(tex)[1:].rsplit("D.")[0]):
#       print(mat, tex)


# from os import scandir
# for mat in mats:
#   match_texture(mat, [f.path for f in scandir(texture_dir)])

# again I want to stress this is not an optimal way to accomplish that specific task
# but its the example I came up with and its fine for that purpose
# another example could be using this in combination with uni_copy 
# to ensure your destination file is only made up of ascii letters if it has a mix of both
# which really only matters if your endpoint is another python package that breaks with nonascii
# e.g. if you're copying files to a useable path for pyinjector
# in that case you should just use a better injection method but I digress
