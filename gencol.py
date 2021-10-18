from os import listdir
import os
from os.path import isfile, join
from PIL import Image

print(os.getcwd())

path = 'C:\\Users\\regis\\PycharmProjects\\gencol\\images'

dic_images ={}
subfolders =  [(f.path,f.name) for f in os.scandir(path) if f.is_dir() ]
print(subfolders)
for f in subfolders:
    my_path = os.path.join(path, f[1])
    onlyfiles = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    dic_images[f[1]] = onlyfiles
print(dic_images)
