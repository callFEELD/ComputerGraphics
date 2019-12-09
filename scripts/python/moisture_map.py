"""
This scripts implements the Moisture Map with Perlin-Noise
This script is part of the exercise 2.1

This script is only executeable in blender.

On executing this script will generate a predefined
moisture map based on the perlin noise algorithm.

Perlin-Noise Algorithm:         https://en.wikipedia.org/wiki/Perlin_noise#Algorithm_detail
Blender Mathutils Noise API:    https://docs.blender.org/api/current/mathutils.noise.html
"""

# This mathutils only contains noise, when executed in blender
import mathutils

# This imports the utils script containing crucial functionality
# for this script. Please start the blender file in the root
# folder, where it is located.
import sys
sys.path.append("./scripts/python")

from utils import save_texture, normalize


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
    noise_map = [[0 for x in range(width)] for y in range(height)]

    # use a random seed for the random noise generator
    mathutils.noise.seed_set(0)
    
    # adding the noise to each pixel of the noise map
    for y in range(height):
        for x in range(width):
            nx = x/width * scale
            ny = y/height * scale
            noise_map[y][x] = mathutils.noise.noise(mathutils.Vector((nx, ny, 1)))
    
    return normalize(noise_map)


if __name__ == "__main__":
    moisture_map = generate_noise_map(1024, 1024, 5)
    save_texture(moisture_map, "//textures/moisture/moisture_map.png")
