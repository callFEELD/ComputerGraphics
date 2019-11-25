# 0,0 is the left upper edge, x defines vertical coordinates downwards, y the horizontal coordinates to the right

import numpy as np
import bpy

import sys
sys.path.append("./scripts/python")

from moisture_map import save_texture, normalize

TEXTURE_SIZE = 17  # 32769 1025 5 17
RANDOM_LOWER = -1
RANDOM_UPPER = 1

# Initialize Array with Zeros
arr = np.zeros(shape=(TEXTURE_SIZE,TEXTURE_SIZE))

# Performs Diamond-Square algorithm
def diamond_square():
    # Seed the 4 corners with random values
    arr[0][0] = np.random.uniform(0, 10)
    arr[0][TEXTURE_SIZE-1] = np.random.uniform(0, 10)
    arr[TEXTURE_SIZE-1][0] = np.random.uniform(0, 10)
    arr[TEXTURE_SIZE-1][TEXTURE_SIZE-1] = np.random.uniform(0, 10)


    step_size = TEXTURE_SIZE - 1

    while step_size > 1:
        print("New Loop; Stepsize: " , step_size)
        halfstep = int(step_size / 2)
        # Loop through diamond step
        for x in range(0,TEXTURE_SIZE-1,step_size):
            for y in range(0,TEXTURE_SIZE-1,step_size):
                diamond(x,y,step_size)
        
        
        is_even = True
        for x in range(0, TEXTURE_SIZE, halfstep):
            for y in range(halfstep if is_even else 0, TEXTURE_SIZE, step_size):
                square(x, y, step_size)
            is_even = not is_even
        step_size = int(step_size/2)



# Performs diamond step, 
def diamond(x, y, step_size):
    # defines corners of the diamond | tl=top left; tr=top right; bl=bottom left; br=bottom right
    tl = arr[x][y]
    tr = arr[x][y+step_size]
    bl = arr[x+step_size][y]
    br = arr[x+step_size][y+step_size]

    # Calculate average
    avg = (tl + tr + bl + br) / 4

    # Calculate final value by adding random value
    fin = avg + np.random.uniform(RANDOM_LOWER *2, RANDOM_UPPER*2)

    # Write final value to array
    arr[int(x+step_size/2)][int(y+step_size/2)] = fin

# Performs square step; x and y represent the middle upper corner of a diamond
def square(x, y, step_size):
    # Calculate half a step, needed to get the values from the middle of the diamon
    halfstep = step_size / 2

    # Get the corner values
    top = arr[int(x-halfstep)][y] if (x-halfstep)>=0 else 0
    bottom = arr[int(x+halfstep)][y] if (x+halfstep)<=TEXTURE_SIZE-1 else 0
    left = arr[x][int(y-halfstep)] if (y-halfstep)>=0 else 0
    right = arr[x][int(y+halfstep)] if (y+halfstep)<=TEXTURE_SIZE-1 else 0

    # Calculate average
    avg = (top + bottom + left + right) / 4

    # Calculate final value by adding random value
    fin = avg + np.random.uniform(RANDOM_LOWER, RANDOM_UPPER)

    arr[x][y] = fin

diamond_square()
arr_norm = normalize(arr)
for i in arr_norm:
    print(i)
save_texture(arr_norm,"//heightmap.png")