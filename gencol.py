import os

class gencol():

    def __init__(self,path):
        self.path = path
        self.all_features = {}

    def get_content(self):
        self.all_features = dict((f.name, features(f.name, f.path)) for f in os.scandir(self.path) if f.is_dir())
        for i, folder in enumerate(self.all_features.values()):
            folder._order = i+1
            folder.project = self

    def featurePos(self,name:str,pos:int):
        if name in self.all_features:
            self.all_features[name].order = pos
        else:
            raise Exception(f"{name} is not a folder in {self.path}")

class features():

    def __init__(self,name,path):
        self.name = name
        self.path = path
        self.mandatory = True
        self._order = None
        self.project = None
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
            raise Exception(f"The position of the feature must be between"\
                            f" the range of features: {len(self.project.all_features)}")

    @order.deleter
    def radius(self):
        print("Delete radius")
        del self._order



test = gencol('C:\\Users\\regis\\PycharmProjects\\gencol\\images')
test.get_content()
print (test.all_features)
for feature in test.all_features:
    print(feature, test.all_features[feature].order)
test.featureOrder('background',2)
for feature in test.all_features:
    print(feature, test.all_features[feature].order)

