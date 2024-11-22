from os.path import join, isdir, abspath, basename
import numpy as np
from PIL import Image
from os import scandir, makedirs, system, rename, getcwd

images = []
imagenames = []


system("texconv -f BC7_UNORM *.png")


def im_has_alpha(img_arr):
    """
    returns True for Image with alpha channel
    """
    try:
        h, w, c = img_arr.shape
        return True if c == 4 else False
    except Exception as e:
        return False

if not isdir(folder:= join(getcwd(), "trans")):
    makedirs(folder)

for image in scandir(getcwd()):
    if image.name.endswith("BC7_UNORM.png"):
        try:
            img = Image.open(image)
            if im_has_alpha(np.array(img)):
                imagenames.append(image.name)
                images.append(img)
                fullname = abspath(image.name)
                newname = join(folder, basename(image.name))
                rename(fullname, newname)
        except Exception as e:
            pass


for f in imagenames:
    print(f)
