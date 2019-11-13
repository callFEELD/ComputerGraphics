"""
This scripts implements the Moisture Map with Perlin-Noise

This script is part of the exercise 2.1

Basic tutorial of noise:        https://www.redblobgames.com/maps/terrain-from-noise/#noise
Perlin-Noise Algorithm:         https://en.wikipedia.org/wiki/Perlin_noise#Algorithm_detail

Blender Mathutils Noise API:    https://docs.blender.org/api/current/mathutils.noise.html
"""

# import standard packages
import bpy
import numpy as np
import mathutils


def generate_noise_map(heigth, width):
    """
    This functions generates a Noise map with values between 0 and 1.
    
    :param heigth: Height of the noise map
    :param width: Width of the noise map
    :return: Map with values between 0 and 1 (greyscale image)
    """
    # init the noisemap with zeros
    noise_map = [[0 for y in range(heigth-1)] for x in range(width-1)]
    
    # adding the noise to each pixel of the noise map
    for y in range(heigth -1):
        for x in range(width -1):
            nx = x/width -0.5
            ny = y/heigth -0.5
            noise_map[y][x] = mathutils.noise.noise(mathutils.Vector((nx, ny, 1)))
    
    return noise_map
