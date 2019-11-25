"""
This scripts implements the Moisture Map with Perlin-Noise
This script is part of the exercise 2.1

This script is only executeable in blender.

Basic tutorial of noise:        https://www.redblobgames.com/maps/terrain-from-noise/#noise
Perlin-Noise Algorithm:         https://en.wikipedia.org/wiki/Perlin_noise#Algorithm_detail

Blender Mathutils Noise API:    https://docs.blender.org/api/current/mathutils.noise.html
"""

import bpy
import numpy as np
# This mathutils only contains noise, when executed in blender
import mathutils

#from Utilities import save_texture


def save_texture(texture_data, filename):
    """
    This functions stores 2d arrays (images) into an image.
    
    :param texture_data: numpy array
    :param filename: filname (path) of the file
    """
    height, width = len(texture_data[0]), len(texture_data)

    # blank image
    image = bpy.data.images.new(filename, width=width, height=height)

    # create black and white image, based of an rgba vector
    image_pixel = [0 for y in range(height) for x in range(width)]
    for y in range(height):
        for x in range(width):
            r = texture_data[x][y]
            g = r
            b = r
            a = 1

            image_pixel[int((x * height) + y)] = [r, g, b, a]

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


def generate_noise_map(height, width, scale):
    """
    This functions generates a Noise map with values between 0 and 1.
    
    This function must be called in blender 2.8 in order to use the 
    mathutils.noise function.
    The normal mathutils library does not support this feature.
    
    :param height: Height of the noise map
    :param width: Width of the noise map
    :param scale: Scale of the perlin noise
    :return: Map with values between 0 and 1 (greyscale image)
    """
    height = int(height)
    width = int(width)
    # init the noisemap with zeros
    noise_map = [[0 for y in range(height)] for x in range(width)]
    
    # adding the noise to each pixel of the noise map
    for y in range(height):
        for x in range(width):
            nx = x/width * scale
            ny = y/height * scale
            noise_map[y][x] = mathutils.noise.noise(mathutils.Vector((nx, ny, 1)))
    
    return normalize(noise_map)


if __name__ == "__main__":
    moisture_map = generate_noise_map(1024, 1024, 20)
    save_texture(moisture_map, "textures/moisture/moisture_map.png")
