# gencol

Module to generate collection of images based on different attributes. The idea is to do something similar to the cryptopunk collection.

It allows to set the rarity of class attribute or of a specific attribute.
For example, if I have a hat attribute then I can set how often a hat will be generated on the final collection.
Same thing for a specific hat, if I want that a blue hat be less generated than other hats, I can see its rarity parameter to a lesser value.

To start a Gencol project, first you need to have all your images in their respective class attribute folders. See demo folder.
```
from gencol import Gencol
mycol = Gencol(your_demo_folder_equivalent')
mycol.get_content()
```
After this all features and the images they contain are converted into Feature and Image objects.
