from __future__ import annotations
from random import choices, randint
from typing import Optional
from PIL import Image as Img
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
        if not os.path.isdir('collection'):
            os.mkdir('collection')

    def get_content(self) -> Gencol:
        """Creates features and Image object based on the path given in the Gencol object.
        """
        self.all_features = dict((feature.name, Feature(feature.name, feature.path, self))
                                 for feature in os.scandir(self.path) if feature.is_dir())

        for i, folder in enumerate(self.all_features.values()):
            folder._position = i+1  # Set the feature.position based on system folder sorting
            folder.all_images = dict((img.name.split('.')[0], Image(img.name, img.path, folder))
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

    def mandatory(self, name: str, set: bool = True) -> Gencol:
        """ Set the mandatory attribute to a feature
        If set to True, the feature will appear in all generated images.
        If set to False, the feature will appear randomly on generated images.
        """
        self.all_features[name].mandatory = set
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

    def get_feature(self,feature: str) -> Feature:
        """ Takes a feature name and returns its Feature object instance"""
        feature = self.all_features[feature]
        return feature

    def get_image(self,feature:str, img_name:str) -> Image:
        """ Takes a feature name and an image name, and returns its Image object instance"""
        img = self.all_features[feature].all_images[img_name]
        return img
    def max_images(self) -> int:
        max_features = [x for x in self.all_features.values() if x.rarity != 0]
        total = 1
        for feature in max_features:
            max_nb_of_images = [x for x in feature.all_images.values() if x.rarity != 0]
            if feature.rarity != 100:
                total = total * (len(max_nb_of_images)+1)
            else:
                total = total * len(max_nb_of_images)

        return total

    def generate_collection(self, nb_to_generate: Optional[int] = None):

        def use_of_feature(feature) -> bool:
            return randint(1, 100) <= feature.rarity

        def get_random_image(images: dict) -> Image:
            img_choices = [x for x in images.values()]
            img_weights = [x.rarity for x in img_choices]
            return choices(img_choices, img_weights)[0]

        if not nb_to_generate:
            nb_to_generate = Gencol.max_images(self)

        for n in range(nb_to_generate):
            while True:
                background: Optional[Img] = None
                compiled_image: list[str] = []
                for feature in self.all_features.values():
                    if use_of_feature(feature):
                        img = get_random_image(feature.all_images)
                        if feature.position == 1:
                            background = Img.open(img.path)
                            compiled_image.append(img.name)
                        else:
                            img_to_add = Img.open(img.path)
                            compiled_image.append(img.name)
                            background.paste(img_to_add, (0, 0), img_to_add)
                filename = f'{"-".join(compiled_image)}.png'
                if not os.path.isfile(f'collection/{filename}'):
                    background.save(f'collection/{filename}')
                    break


class Feature:

    def __init__(self, name: str, path: str, project: Gencol):
        self.name = name
        self.path = path
        self.rarity = 100  # How likely to have this feature in the final generated image
        self._position = None  # position of the feature when overlaid with other features
        self.project = project
        self.all_images = {}

    @property
    def rarity(self):
        """The rarity property."""
        return self._rarity

    @rarity.setter
    def rarity(self, value: int):
        if 0 <= value <= 100:
            self._rarity = value
        else:
            raise ValueError('The rarity is an integer between 0 and 100 included')

    @property
    def position(self):
        """The position property."""
        return self._position

    @position.setter
    def position(self, value: int):
        """Set new position of a feature
        When a new position is set, the position of the feature which was originally
        on the new position is moved by one towards the original position of the feature
        for which the method has been called.
        Ex: 4 features with positions, 1,2,3 and 4.
        If we call this method for the feature on 3rd position with a new position of 1.
        The feature which was on 1st position will move to 2nd, and the one on 2nd to 3rd.
        """

        if value < len(self.project.all_features)+1:
            self._position = value
            positions: list[int] = [feature.position for feature in self.project.all_features.values()]
            old_position: int = Feature.find_empty_position(positions, self._position)
            for feature in self.project.all_features.values():
                if feature.name != self.name and feature.position == value:
                    if old_position>value:
                        feature.position += 1
                    elif old_position<value:
                        feature.position -= 1

        else:
            raise Exception(f"The position of the feature must be between "
                            f"the range of features: {len(self.project.all_features)}")

    @staticmethod
    def find_empty_position(positions:list[int],old_position:int)->int:
        for i, x in enumerate(positions):
            if i + 1 not in positions: return i + 1
        return old_position

    def get_image(self, img_name:str) -> Image:
        """ Takes an image name, and returns its Image object instance"""
        img = self.all_images[img_name]
        return img


class Image:

    def __init__(self, name, path, feature):
        self.name, self._format = name.split('.')
        self.path = path
        self.rarity = 100
        self.feature = feature

    @property
    def format(self):
        """The format property."""
        return self._format

    @property
    def rarity(self):
        """The rarity property."""
        return self._rarity

    @rarity.setter
    def rarity(self, value: int):
        if 0 <= value <= 100:
            self._rarity = value
        else:
            raise ValueError('The rarity is an integer between 0 and 100 included')




