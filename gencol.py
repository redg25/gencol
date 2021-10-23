import os

class gencol():

    def __init__(self,path):
        self.path = path
        self.name = self.path.split('\\')[-1]
        self.all_features = {}

    def get_content(self):
        '''
        Creates features and Image object based on the path given in the gencol object.
        All features are the list of all subfolders
        All Image are the images in those subfolders
        :return:
        '''
        self.all_features = dict((f.name, features(f.name, f.path,self)) for f in os.scandir(self.path) if f.is_dir())
        for i, folder in enumerate(self.all_features.values()):
            folder._order = i+1 #Set the feature.order based on system folder sorting
            folder.all_images = dict((img.name, Image(img.name, img.path, folder))
                                     for img in os.scandir(folder.path) if not img.is_dir())

    def feature_pos(self,name:str,pos:int):
        if name in self.all_features:
            self.all_features[name].order = pos
        else:
            raise Exception(f"{name} is not a folder in {self.path}")

class features():

    def __init__(self,name,path,project):
        self.name = name
        self.path = path
        self.mandatory = True
        self._order = None
        self.project = project
        self.all_images = {}

    @property
    def order(self):
        """The order property."""
        return self._order

    @order.setter
    def order(self, value):
        if value < len(self.project.all_features):
            self._order = value
        else:
            raise Exception(f"The position of the feature must be between "
                            f"the range of features: {len(self.project.all_features)}")

    @order.deleter
    def radius(self):
        print("Delete radius")
        del self._order

class Image():

    def __init__(self, name, path, feature):
        self.name = name
        self.path = path
        self.rarity = 100
        self.feature = feature

test = gencol('C:\\Users\\regis\\PycharmProjects\\gencol\\images')
test.get_content()
print (test.all_features)
# for feature in test.all_features:
#     print(feature, test.all_features[feature].order)
#test.feature_pos('backgrounds',2)
# for feature in test.all_features.values():
#     print (feature)
#     # print(feature., test.all_features[feature].order)
#     names = [x.name for x in feature.all_images.values()]
#     print (f'{feature.name}: {names}')
print (test.name)
for feature,value in test.all_features.items():
    print(f'{feature}:\n'
          f'Mandatory is {value.mandatory}\n'
          f'Order is {value.order}')
    for image, v in value.all_images.items():
        print(f'{image}:\n'
              f'rarity is {v.rarity}')


