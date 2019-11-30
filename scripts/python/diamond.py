import numpy as np
import bpy

import sys
sys.path.append("./scripts/python")

from moisture_map import save_texture, normalize

# Performs Diamond-Square algorithm
def diamond_square_main(arr, random_upper, random_lower, dividor_multiplier, seed_lower, seed_upper, tex_size):
    """Main Method of the Diamond-Square Algorithm
    
    Arguments:
        arr {2d float array} -- Array which defines the heightmap
        random_upper {float} -- upper value of the random generator
        random_lower {float} -- lower value of the ranodm generator
        dividor_multiplier {[type]} -- [description]
        seed_lower {[type]} -- [description]
        seed_upper {[type]} -- [description]
        tex_size {[type]} -- [description]
    
    Returns:
        float array -- Array which defines the heightmap with the diamond-square algorithm applied
    """

    # Seed the 4 corners with random values
    arr[0][0] = np.random.uniform(seed_lower,seed_upper)
    arr[0][tex_size-1] = np.random.uniform(seed_lower, seed_upper)
    arr[tex_size-1][0] = np.random.uniform(seed_lower, seed_upper)
    arr[tex_size-1][tex_size-1] = np.random.uniform(seed_lower, seed_upper)


    step_size = tex_size - 1
    dividor = 1

    while step_size > 1:
        print("New Loop; Stepsize: " , step_size)
        halfstep = int(step_size / 2)
        # Loop through diamond step
        for x in range(0,tex_size-1,step_size):
            for y in range(0,tex_size-1,step_size):
                arr = diamond(arr, x,y,step_size,dividor, random_upper, random_lower)
        
        
        is_even = True
        for x in range(0, tex_size, halfstep):
            for y in range(halfstep if is_even else 0, tex_size, step_size):
                square(arr, x, y, step_size,dividor, random_upper, random_lower, tex_size)
            is_even = not is_even
        step_size = int(step_size/2)
        dividor = dividor*dividor_multiplier
    return arr



# Performs diamond step, 
def diamond(arr, x, y, step_size, dividor, random_upper, random_lower):
    """Performs the diamond step of the diamons-square algorithm
    
    Arguments:
        arr {2d float array} -- Array which defines the heightmap
        x {int} -- X coordinate
        y {int} -- Y coordinate
        step_size {int} -- step size of the current interation
        dividor {float} -- value by which the random boundries are divided
        random_upper {float} -- upper value of the random generator
        random_lower {float} -- lower value of the ranodm generator
        tex_size {int} -- size of the texture/heightmap
    
    Returns:
        float array -- Array which defines the heightmap with the diamond step applied
    """

    # defines corners of the diamond | tl=top left; tr=top right; bl=bottom left; br=bottom right
    tl = arr[x][y]
    tr = arr[x][y+step_size]
    bl = arr[x+step_size][y]
    br = arr[x+step_size][y+step_size]

    # Calculate average
    avg = (tl + tr + bl + br) / 4

    # Calculate final value by adding random value
    fin = avg + np.random.uniform(random_lower/dividor, random_upper/dividor)

    # Write final value to array
    arr[int(x+step_size/2)][int(y+step_size/2)] = fin
    return arr

def square(arr, x, y, step_size, dividor, random_upper, random_lower, tex_size):
    """Performs the square step of the diamons-square algorithm
    
    Arguments:
        arr {2d float array} -- Array which defines the heightmap
        x {int} -- X coordinate
        y {int} -- Y coordinate
        step_size {int} -- step size of the current interation
        dividor {float} -- value by which the random boundries are divided
        random_upper {float} -- upper value of the random generator
        random_lower {float} -- lower value of the ranodm generator
        tex_size {int} -- size of the texture/heightmap
    
    Returns:
        float array -- Array which defines the heightmap with the diamond step applied
    """

    # Calculate half a step, needed to get the values from the middle of the diamon
    halfstep = step_size / 2

    # Get the corner values
    top = arr[int(x-halfstep)][y] if (x-halfstep)>=0 else 0
    bottom = arr[int(x+halfstep)][y] if (x+halfstep)<=tex_size-1 else 0
    left = arr[x][int(y-halfstep)] if (y-halfstep)>=0 else 0
    right = arr[x][int(y+halfstep)] if (y+halfstep)<=tex_size-1 else 0

    # Calculate average
    avg = (top + bottom + left + right) / 4

    # Calculate final value by adding random value
    fin = avg + np.random.uniform(random_lower/dividor, random_upper/dividor)

    arr[x][y] = fin
    return arr


def diamond_square(width, height, random_upper, random_lower, dividor_multiplier, seed_lower, seed_upper, save_path):
    """
    Main method for running the diamond-square algorithm
        :param width: width of the heightmap
        :param height: height of the heightmap
        :param random_upper: highest value of the random generator
        :param random_lower: lowest value of the random generator
        :param dividor_multiplier: multiplies the divider each iteration; The dividor is applied to the random boundries
        :param seed_lower: lower value for generating the seed
        :param seed_upper: upper value for generating the seed
        :param save_path: path to save the file to, "//heightmap.png" if string is empty
    """
    
    
    # Create tex_size variable to store the width and height of the heightmap which will be generated
    # This is necessary as the algorithm can only use a limited set of sizes of the heightmap
    tex_size = 0
    
    for i in range(1,20):
        print("testing n=",i)
        ds_value = np.power(2, i) + 1
        if ds_value >= width and ds_value >= height:
            tex_size = ds_value
            break
    print("Texture size: ", tex_size)
    
    # Initialize Array with Zeros
    arr = np.zeros(shape=(tex_size,tex_size))
    
    # run diamond square algorithm
    arr = diamond_square_main(arr, random_upper, random_lower, dividor_multiplier, seed_lower, seed_upper, tex_size)
    

    # Cut the array to the desired width and height
    cut_arr = np.zeros(shape=(height,width))
    for i in range(height):
        for j in range(width):
            cut_arr[i][j] = arr[i][j]

    arr_norm = normalize(cut_arr)
    if (save_path == ""):
        save_path = "//heightmap.png"
    save_texture(arr_norm,save_path)
    

# Example method call
# wdiamond_square(1920,1080,5,-5,2,0,5,"")