import numpy as np

def expand(selection, radius):
    # https://stackoverflow.com/questions/64052589/expand-a-selection-of-pixels-in-opencv-2
    cop = np.copy(selection)
    for x in range(-radius,radius+1):
        for y in range(-radius,radius+1):
            if (y==0 and x==0) or (x**2 + y**2 > radius **2):
                continue
            shift = np.roll(np.roll(selection, y, axis = 0), x, axis = 1)
            cop += shift

def expand_black_area(image, iderations):
    x_max, y_max = np.shape(image)
    x_max -= 1
    y_max -= 1
    for i in range(iderations):
        original = np.copy(image)
        for pixal in np.ndenumerate(image):
            x = pixal[0][0]
            y = pixal[0][1]
            for x_shift, y_shift in [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]:
                if((0 > x + x_shift) or  (x + x_shift) > x_max or (0 > y + y_shift) or (y + y_shift) > y_max):
                    pass
                elif (original[x+x_shift,y+y_shift] == 0):
                    image[x,y] = 0
    return image
                    