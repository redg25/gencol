from os import listdir
import os
import re
from os.path import isfile, join
from PIL import Image


class gencol():

    def __init__(self,path):
        self.path = path
        self.all_features = []

    def get_content(self):
        self.all_features = [features(f.path,f.name) for f in os.scandir(self.path) if f.is_dir()]
        for i, folder in enumerate(self.all_features):
            folder.order = i+1
            folder.project = self





    def set_f_order(self,f_name,pos):
        pass



class features():

    def __init__(self,name,path):
        self.name = name
        self.path = path
        self.mandatory = True
        self.order = None
        self.project = None


    def position(self,order):
        self.order =  order



test = gencol('C:\\Users\\regis\\PycharmProjects\\gencol\\images')
test.get_content()
print (test.all_features)
for feature in test.all_features:
    print(feature.name, feature.order)