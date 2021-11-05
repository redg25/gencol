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
                                  'rarity': feature_instance.rarity,
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
        """ Calculate the maximum number of images that can be generated based on rarity of features
        and images
        If a feature has a rarity different from 0 or 100, it means that there can be generated full images
        with all the images of the feature and with none of them.

        :return: total:int
        """
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
        """Generate the collection of images"""

        def use_of_feature(feature: Feature) -> bool:
            """Calculate if a feature has to be used based on its rarity"""
            return randint(1, 100) <= feature.rarity

        def get_random_image(images: dict) -> Image:
            """Get a random image from the list of possible images"""
            img_choices = [img for img in images.values()]
            img_weights = [img.rarity for img in img_choices]
            return choices(img_choices, img_weights)[0]

        def order_features_by_position(project:Gencol) -> list[Gencol]:
            """Order the features by their position parameter"""
            lst = [feature for feature in project.all_features.values()]
            lst.sort(key=lambda x: x.position)
            return lst

        if not nb_to_generate:
            nb_to_generate = Gencol.max_images(self)

        for n in range(nb_to_generate):
            while True:
                background: Optional[Img] = None  # Background image to receive the next layer of image(s)
                # List of the different image names included in the image being generated
                compiled_image: list[str] = []
                for feature in order_features_by_position(self):
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




