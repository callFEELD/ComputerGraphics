"""
This script exports the texture (numpy file) moisture map file 
to image file containing the moisture map

This script can only be called outside of blender, since matplotlib
is not accesable inside blender.
"""

import numpy as np
from PIL import Image

if __name__ == '__main__':
    TEXTURE_FILE = 'textures/moisture_map.npy'
    IMAGE_FILE = 'textures/moisture_map.png'

    I = np.load(TEXTURE_FILE)
    
    # greyscale
    I8 = (((I - I.min()) / (I.max() - I.min())) * 255.9).astype(np.uint8)
    img = Image.fromarray(I8)

    img.save(IMAGE_FILE)