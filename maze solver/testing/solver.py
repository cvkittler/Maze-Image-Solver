import os
import cv2
import numpy as np
from PIL import Image
from testing.helperFunctions import *

FILE_NAME = "maze2"
FILE_TYPE = ".png"
im_gray = np.array(Image.open(FILE_NAME + FILE_TYPE).convert('L'))

maxval = 255
thresh = 128
print("Making Temp File")
try:
    os.mkdir("./TEMP")
except OSError as error: 
    print(error)  

print("Binarizing Image")
im_bin = (im_gray > thresh) * maxval
print("\tDone Binarizing")

print("Cropping Image")
x, y = np.shape(im_bin)
top_padding = left_padding = 0
right_padding = x - 1
bottom_padding = y - 1
while (im_bin[int(x/2)][top_padding]):
    top_padding += 1
while (im_bin[left_padding][int(y/2)]):
    left_padding += 1
while (im_bin[int(x/2)][bottom_padding]):
    bottom_padding -= 1
while (im_bin[right_padding][int(y/2)]):
    right_padding -= 1
Image.fromarray(np.uint8(im_bin[left_padding:right_padding, top_padding:bottom_padding])).save("./TEMP/" + FILE_NAME + '_BINARIZED' + FILE_TYPE)

cropped_img = im_bin[left_padding:right_padding, top_padding:bottom_padding]
print("\tDone Cropping")

print("Expanding the binerized image")
expanded = expand_black_area(cropped_img,3)
cv2.imwrite("./TEMP/" + FILE_NAME + '_BINARIZED_EXPANDED' + FILE_TYPE, expanded)
print("\tDone Expanding")

print("Removeing small blobs")
#find all your connected components (white blobs in your image)
expanded = (expanded/255)
nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(expanded, connectivity=8)
#connectedComponentswithStats yields every seperated component with information on each of them, such as size
#the following part is just taking out the background which is also considered a component, but most of the time we don't want that.
sizes = stats[1:, -1]; nb_components = nb_components - 1

# minimum size of particles we want to keep (number of pixels)
#here, it's a fixed value, but you can set it as you want, eg the mean of the sizes or whatever
min_size = 50  

#your answer image
img2 = np.zeros((output.shape))
#for every component in the image, you keep it only if it's above min_size
for i in range(0, nb_components):
    if sizes[i] >= min_size:
        img2[output == i + 1] = 255

cv2.imwrite("./TEMP/" + FILE_NAME + '_BINARIZED_BLOBS_REMOVED' + FILE_TYPE, img2)

print("Searching for start and end")
x, y = np.shape(cropped_img)
x -= 1
y -= 1
print("\tMax array indexex",x,y)
print("\tFinding Start:")
start = [0,0]
for x_index in range(x-1):
    if cropped_img[x_index, 0] and cropped_img[x_index + 1, 0]:
        start = [x_index,0]
for y_index in range(y-1): 
    if cropped_img[0, y_index] and cropped_img[0, y_index + 1]:
        start = [0, y_index]

if start == [0,0]:
    print("\tStart Not Found Continuing search")
else:
    print("\t\tFound start at ", start)

print("\tFinding End:")
end = [x,y]
for x_index in range(x-1, 0, -1):
    if cropped_img[x_index, y] and cropped_img[x_index - 1, y]:
        end = [x_index, y]
for y_index in range(y-1, 0, -1):
    if cropped_img[x, y_index] and cropped_img[x, y_index - 1]:
        end = [x, y_index]

if end == [x,y]:
    print("\t\tEnd Not Found Continuing search")
else:
    print("\t\tFound End at ", end)
