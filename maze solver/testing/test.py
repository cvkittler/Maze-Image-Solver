from copy import deepcopy
from PIL import Image
import numpy as np
arrayBase = np.ones((25,25,1),dtype="uint8")
array = np.ones((25,25,1))
for i in range(200):
    array = np.append(array, arrayBase*i,axis=1)
print(array)
image = Image.fromarray(np.uint8(array))
image.save("./TEMP/test.gif")
