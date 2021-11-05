# gencol

Module to generate collection of images based on different attributes. The idea is to do something similar to the cryptopunk collection.

It allows to set the rarity of class attribute or of a specific attribute.
For example, if I have a hat attribute then I can set how often a hat will be generated on the final collection.
Same thing for a specific hat, if I want that a blue hat be less generated than other hats, I can set its rarity parameter to a lesser value.

To start a Gencol project, first you need to have all your images in their respective class attribute folders. See demo folder.
```
from gencol import Gencol
mycol = Gencol(your_demo_folder_equivalent')
mycol.get_content()
```
After this all features and the images they contain are converted into Feature and Image objects.

You can access a Feature with
```
f1 = mycol.get_feature('feature name') # You can use '**eyes**' with the demo sample
```

and an Image with
```
img1 = mycol.get_image('name of feature','name of image') You can use '**eyes**' and '**eyes1**' with the demo sample
img2 = f1.get_image('name of image') # You can use '**eyes1**' with the demo sample
```

By default, all features and images have rarity set to 100 which means all possible scenarios will be generated.
If you want a feature to be rare, you can set the rarity with

```
f1.rarity = 80  # the feature will be generated 80% of the time 
img1.rarity = 20  # When chosing an image randomly the rarity will be weighted against other image rarities
```

The order in which the feature are generated is originally set by your system, for exampe if you want hats to be over the main face
then hats position should be at least one positon higher than the main face. 
You can change it with
```
f1.position = 5
```
Note that other impacted features will be moved by one up or down depending toward which direction the feature you changed is going.

To generate a collection of images:
```
mycol.generate_collection(nb_to_generate=None)
```
It will saves all png images in the collection folder which has been created on the creation of the Gencol object.
If the **nb_to_generate** parameter is not given, all the possible comninations will be generated, except for feature and images where the rariry has bee set to 0.

Extras features:

Get the maximum number of images
```
nb_max = mycol.max_images()
```

Get a json of the structure of the project
```
mycol.get_json()
myjson = mycol.json
```
**You can see all generated images from the demo in the collection folder**
