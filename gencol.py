import os
import json


class Gencol:
    """Class representing a collection generator project.
    Params:
        - path: The path of the project folder
    """
    def __init__(self, path):
        self.path = path
        # Equals the last sub folder name in the path
        self.name = self.path.split('\\')[-1]
        # Represents all the sub folders in the project folder
        self.all_features = {}
        self.json = None

    def get_content(self):
        """Creates features and Image object based on the path given in the Gencol object.
        """
        self.all_features = dict((feature.name, Feature(feature.name, feature.path, self))
                                 for feature in os.scandir(self.path) if feature.is_dir())

        for i, folder in enumerate(self.all_features.values()):
            folder._order = i+1  # Set the feature.order based on system folder sorting
            folder.all_images = dict((img.name, Image(img.name, img.path, folder))
                                     for img in os.scandir(folder.path) if not img.is_dir())

    def feature_pos(self, name: str, pos: int):
        if name in self.all_features:
            if self.all_features[name].order < pos:
                for feature in self.all_features.values():
                    if feature.name != name and feature.order <= pos and feature.order > self.all_features[name].order:
                        feature.order -= 1
            elif self.all_features[name].order > pos:
                for feature in self.all_features.values():
                    if feature.name != name and feature.order >= pos and feature.order < self.all_features[name].order:
                        feature.order += 1
            self.all_features[name].order = pos

        else:
            raise Exception(f"{name} is not a folder in {self.path}")

    def get_json(self):
        """Create a json object with the structure of the project and the attributes of each element"""
        project_dict = {}
        for feature, feature_instance in self.all_features.items():
            # For a feature, to create a dictionary with image names as keys
            # and their attributes as a dictionary for values
            images = dict((img, {'path': img_instance.path,
                                 'rarity': img_instance.rarity})
                          for img, img_instance in feature_instance.all_images.items())
            # To add a feature as a key in the project_dict
            # and its attributes as a dictionary for values.
            # The value for the images attribute is the "images" dictionary
            project_dict[feature] = {'path': feature_instance.path,
                                     'mandatory': feature_instance.mandatory,
                                     'position': feature_instance.order,
                                     'images': images}

        self.json = json.dumps(project_dict, indent=4)


class Feature:

    def __init__(self, name, path, project):
        self.name = name
        self.path = path
        self.mandatory = True  # Is this feature required in all generated images?
        self._order = None  # Order of the feature when overlaid with other features
        self.project = project
        self.all_images = {}

    @property
    def order(self):
        """The order property."""
        return self._order

    @order.setter
    def order(self, value):
        if value < len(self.project.all_features)+1:
            self._order = value
        else:
            raise Exception(f"The position of the feature must be between "
                            f"the range of features: {len(self.project.all_features)}")

    @order.deleter
    def radius(self):
        print("Delete radius")
        del self._order


class Image:

    def __init__(self, name, path, feature):
        self.name = name
        self.path = path
        self.rarity = 100
        self.feature = feature

test = Gencol('C:\\Users\\regis\\PycharmProjects\\gencol\\images')
test.get_content()
#test.get_json()
# with open('test.json','w') as outfile:
#     outfile.write(test.pjson)
# print (test.all_features)
for feature in test.all_features:
    print(feature, test.all_features[feature].order)

test.feature_pos('f2_mouths',2)
for feature in test.all_features:
    print(feature, test.all_features[feature].order)
# #     names = [x.name for x in feature.all_images.values()]
# #     print (f'{feature.name}: {names}')
# print (test.name)
# for feature,value in test.all_features.items():
#     print(f'{feature}:\n'
#           f'Mandatory is {value.mandatory}\n'
#           f'Order is {value.order}')
#     for image, v in value.all_images.items():
#         print(f'{image}:\n'
#               f'rarity is {v.rarity}')
#

