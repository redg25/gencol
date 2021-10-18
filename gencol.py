from os import listdir
import os
from os.path import isfile, join
from PIL import Image
print(os.path)
folder = "images"
bg_folder = f'{folder}/backgrounds/)'
onlyfiles = [f for f in listdir(bg_folder) if isfile(join(bg_folder, f))]
