"""
This scripts contains basic utility functions for the mositure map
(perlin noise) and diamond square algorithms.
"""

import bpy
import numpy as np


def save_texture(texture_data, filename):
    """
    This functions stores 2d arrays (images) into an image.
    
    :param texture_data: numpy array
    :param filename: filname (path) of the file
    """
    height, width = len(texture_data), len(texture_data[0])

    # blank image
    image = bpy.data.images.new(filename, width=width, height=height)

    # create black and white image, based of an rgba vector
    image_pixel = [0 for y in range(height) for x in range(width)]
    for y in range(height):
        for x in range(width):
            r = texture_data[y][x]
            g = r
            b = r
            a = 1

            image_pixel[int((y * width) + x)] = [r, g, b, a]

    # make it only 1d for blender
    image_pixel = [color_channel for x in image_pixel for color_channel in x]

    # assign pixels
    image.pixels = image_pixel

    # write image
    image.filepath_raw = filename
    image.file_format = 'PNG'
    image.save()
    

def normalize(texture_map):
    """
    This functions normalize the noise map/texture maps.

    Due to appearing negative numbers, the 2d array must
    be normalized.

    :param texture_map: 2d array, that should be normalized
    :return: normalized 2d array
    """
    # finding the smallest value of the texture map
    smallest_value = np.amin(texture_map)
    # finding the largest value of the texture map
    largest_value = np.amax(texture_map)
    value_range = largest_value + abs(smallest_value)

    # Go through the 2d array and update the values
    # according to the smallest and highest values
    for y in range(len(texture_map)):
        for x in range(len(texture_map[y])):
            # The normalized value is = (current value + the smallest value) / value_range
            texture_map[y][x] = (texture_map[y][x] + abs(smallest_value)) / value_range
    
    return texture_map