from __future__ import annotations

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

    def get_content(self) -> Gencol:
        """Creates features and Image object based on the path given in the Gencol object.
        """
        self.all_features = dict((feature.name, Feature(feature.name, feature.path, self))
                                 for feature in os.scandir(self.path) if feature.is_dir())

        for i, folder in enumerate(self.all_features.values()):
            folder._position = i+1  # Set the feature.position based on system folder sorting
            folder.all_images = dict((img.name, Image(img.name, img.path, folder))
                                     for img in os.scandir(folder.path) if not img.is_dir())

    def feature_pos(self, name: str, new_position: int) -> Gencol:
        """
        Changes the layer on which the feature will be displayed on the final image.
        Other features positions are changed to ensure that none have the same position.
        :param name: The name of the feature
        :param new_position: The layer position of the feature on a full generated image.
        :return: self
        """
        if name in self.all_features:
            # Check if new position is after current position.
            if self.all_features[name].position < new_position:
                for feat in self.all_features.values():
                    # Check what other feature are impacted and move their position down by 1
                    if feat.name != name and new_position >= feat.position > self.all_features[name].position:
                        feat.position -= 1
            # Check if new position is before current position.
            elif self.all_features[name].position > new_position:
                for feat in self.all_features.values():
                    # Check what other feature are impacted and move their position up by 1
                    if feat.name != name and new_position <= feat.position < self.all_features[name].position:
                        feat.position += 1
            # Set new position of the feature
            self.all_features[name].position = new_position

        else:
            raise Exception(f"{name} is not a folder in {self.path}")
        return self

    def get_json(self) -> Gencol:
        """Create a json object with the structure of the project and the attributes of each element"""
        project_dict = {}
        for name, feature_instance in self.all_features.items():
            # For a feature, to create a dictionary with image names as keys
            # and their attributes as a dictionary for values
            images = dict((img, {'path': img_instance.path,
                                 'rarity': img_instance.rarity})
                          for img, img_instance in feature_instance.all_images.items())
            # To add a feature as a key in the project_dict
            # and its attributes as a dictionary for values.
            # The value for the images attribute is the "images" dictionary
            project_dict[name] = {'path': feature_instance.path,
                                  'mandatory': feature_instance.mandatory,
                                  'position': feature_instance.position,
                                  'images': images}

        self.json = json.dumps(project_dict, indent=4)


class Feature:

    def __init__(self, name, path, project):
        self.name = name
        self.path = path
        self.mandatory = True  # Is this feature required in all generated images?
        self._position = None  # position of the feature when overlaid with other features
        self.project = project
        self.all_images = {}

    @property
    def position(self):
        """The position property."""
        return self._position

    @position.setter
    def position(self, value: int):
        if value < len(self.project.all_features)+1:
            self._position = value
        else:
            raise Exception(f"The position of the feature must be between "
                            f"the range of features: {len(self.project.all_features)}")

    @position.deleter
    def radius(self):
        print("Delete radius")
        del self._position


class Image:

    def __init__(self, name, path, feature):
        self.name = name
        self.path = path
        self.rarity = 100
        self.feature = feature

# test = Gencol('C:\\Users\\regis\\PycharmProjects\\gencol\\images')
# test.get_content()
# #test.get_json()
# # with open('test.json','w') as outfile:
# #     outfile.write(test.pjson)
# # print (test.all_features)
# for feature in test.all_features:
#     print(feature, test.all_features[feature].position)
#
# test.feature_pos('f2_mouths',1)
# for feature in test.all_features:
#     print(feature, test.all_features[feature].position)
# # #     names = [x.name for x in feature.all_images.values()]
# # #     print (f'{feature.name}: {names}')
# # print (test.name)
# # for feature,value in test.all_features.items():
# #     print(f'{feature}:\n'
# #           f'Mandatory is {value.mandatory}\n'
# #           f'position is {value.position}')
# #     for image, v in value.all_images.items():
# #         print(f'{image}:\n'
# #               f'rarity is {v.rarity}')
#

