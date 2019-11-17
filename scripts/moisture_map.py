"""
This scripts implements the Moisture Map with Perlin-Noise
This script is part of the exercise 2.1

This script is only executeable in blender.

To get the image file for blender, run the script export_moisture_map.py.

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
    This functions stores 2d arrays (images) into a numpy file.
    After that, the function export_texture() can be called in order
    to save the texture data into a image.
    
    export_texture() can not be called inside blender (since matplotlib
    is not accesable inside blender). Therefore this function is used to
    store the texture data from blender into a file. This file can then
    be converted into an image file outside of blender.
    
    :param texture_data: numpy array
    :param filename: filname (path) of the file
    """
    np.save(filename, texture_data)


def generate_noise_map(height, width):
    """
    This functions generates a Noise map with values between 0 and 1.
    
    This function must be called in blender 2.8 in order to use the 
    mathutils.noise function.
    The normal mathutils library does not support this feature.
    
    :param height: Height of the noise map
    :param width: Width of the noise map
    :return: Map with values between 0 and 1 (greyscale image)
    """
    height = int(height)
    width = int(width)
    # init the noisemap with zeros
    noise_map = [[0 for y in range(height-1)] for x in range(width-1)]
    
    # adding the noise to each pixel of the noise map
    for y in range(height -1):
        for x in range(width -1):
            nx = x/width -0.5
            ny = y/height -0.5
            noise_map[y][x] = mathutils.noise.noise(mathutils.Vector((nx, ny, 1)))
    
    return noise_map


if __name__ == "__main__":
    moisture_map = generate_noise_map(1024, 1024)
    save_texture(moisture_map, "textures/moisture_map")
