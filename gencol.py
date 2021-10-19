from os import listdir
import os
import re
from os.path import isfile, join
from PIL import Image


class gencol():

    def __init__(self,path):
        self.path = path
        self.all_images = {}

    def get_content(self):
        subfolders = [(f.path, f.name) for f in os.scandir(self.path) if f.is_dir()]
        for f in subfolders:
            if re.search("^f\d{1,2}_",f.name):
                pos =f.name.split('_')[0][1:]

            feature = gencol.feature(f.name)
            my_path = os.path.join(self.path, f[1])
            images = [f for f in listdir(my_path) if isfile(join(my_path, f))]
            self.all_images[f[1]] = images

    class features():

        def __init__(self,name):
            self.name = name
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
