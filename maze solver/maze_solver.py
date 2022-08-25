import argparse, os
import numpy as np
from PIL import Image
import cv2 as cv2
from aStarOptimized import aStar, aStarWithImage

args = None

def main():
    parser = argparse.ArgumentParser(description="Solves images of mazes")
    parser.add_argument('-f','--file', type=str, default="maze1.png", help="The path to the maze image")
    debug_help = "0 - No debug 1 - Print statements 2 - Print statements and file outputs"
    parser.add_argument('-d','--debug', type=int, default=2,help=debug_help)

    global args
    args = parser.parse_args()

    if (args.debug >= 1):
        print(args)
    if (args.debug >= 2):
        print("Making Temp Directory")
        try:
            os.mkdir("./TEMP")
        except OSError as error: 
            print(error) 
            files = os.listdir('./TEMP')
            if len(files) > 0:
                print("Cleaning Temp dir")
                for file in files:
                    print("\t Removing file: " + file)
                    os.remove("./TEMP/" + file)
    image = getImage()
    image = makeGrayImage(image)
    image = binarizeImage(image)
    image = cropImage(image)
    image = expandWalls(image,1)
    # image = scaleImage(image,50) 
    start,end = getStartEnd(image)
    runAStar(image,start,end)

def expand_black_area(image, iderations):
    #TODO: Multithread this it's slow
    x_max, y_max = np.shape(image)
    x_max -= 1
    y_max -= 1
    for i in range(iderations):
        print(f"\tExpanded stage {i+1}")
        original = np.copy(image)
        for pixal in np.ndenumerate(image):
            x = pixal[0][0]
            y = pixal[0][1]
            # white it 255
            # black is 0
            for x_shift, y_shift in [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]:
                if(x+x_shift < x_max and y+y_shift < y_max):
                   if 0 == original[x+x_shift][y+y_shift]: #if its black
                       image[x][y] = 0
    return image

def saveTempImage(name, image):
    num = len(os.listdir('./TEMP'))
    image_name = args.file.split("/")[-1].split(".")[0]
    image_file_type = args.file.split("/")[-1].split(".")[-1]
    file_path = "./TEMP/"+str(num)+"_" + image_name + '_'+name+'.' + image_file_type
    Image.fromarray(np.uint8(image)).save(file_path)

def getImage():
    global args
    image = Image.open(args.file)
    if (args.debug >= 1):
        print("Getting Image")
    if (args.debug >= 2):
        saveTempImage("STARTING",image)
    return image

def makeGrayImage(image):
    global args
    im_gray = image.convert('L')
    if (args.debug >= 1):
        print("Making gray scale image")
    if (args.debug >= 2):
        saveTempImage("MONOCHROME",im_gray)
    return im_gray

def binarizeImage(image):
    global args
    image = np.array(image)
    maxval = 255
    thresh = 128
    im_bin = (image > thresh) * maxval
    if (args.debug >= 1):
        print("Binarizing image with threshold of " + str(thresh))
    if (args.debug >= 2):
        saveTempImage("BINARIZED",im_bin)
    return im_bin

def cropImage(image):
    global args
    x, y = np.shape(image)

    top_padding = left_padding = 0
    right_padding = x - 1
    bottom_padding = y - 1
    while (image[int(x/2)][top_padding]):
        top_padding += 1
    while (image[left_padding][int(y/2)]):
        left_padding += 1
    while (image[int(x/2)][bottom_padding]):
        bottom_padding -= 1
    while (image[right_padding][int(y/2)]):
        right_padding -= 1
    
    image = image[left_padding:right_padding, top_padding:bottom_padding]

    if (args.debug >= 1):
        print(f"Cropping image of binarized maze image staring size is [{x}, {y}]" )
        print(f"\tCrop amount from edge")
        print(f"\tTop    crop: {top_padding}")
        print(f"\tBottom crop: {y - bottom_padding}")
        print(f"\tLeft   crop: {left_padding}")
        print(f"\tRight  crop: {x - right_padding}")
    if (args.debug >= 2):
        saveTempImage("CROPPED",image)
    return image

def expandWalls(image,amount):
    if (args.debug >= 1):
        print("Expanded maze walls by " + str(amount))

    expanded = expand_black_area(image,amount)
    
    if (args.debug >= 2):
        saveTempImage("EXPANDED",expanded)

    return expanded

counter = 0
points = []
def mousePointsCallbackSMALL(event,x,y,flags,params):
    global counter
    # Left button mouse click event opencv
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x*2,y*2))
        counter = counter + 1
        if counter == 2:
            cv2.destroyAllWindows() 
            return points

def mousePointsCallbackNORMAL(event,x,y,flags,params):
    global counter
    # Left button mouse click event opencv
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x,y))
        counter = counter + 1
        if counter == 2:
            cv2.destroyAllWindows() 
            return points

def mousePointsCallbackLARGE(event,x,y,flags,params):
    global counter
    # Left button mouse click event opencv
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((int(x/2),int(y/2)))
        counter = counter + 1
        if counter == 2:
            cv2.destroyAllWindows() 
            return points

def scaleImage(image, scale):
    scale_percent = scale
    width = int(np.shape(image)[1] * scale_percent / 100)
    height = int(np.shape(image)[0] * scale_percent / 100)
    dim = (width, height)
    
    imS = cv2.resize(image.astype('float32'), dim)
    return imS

def getStartEnd(image):
    if (args.debug >= 1):
        print("Getting Start and end Positions")
    image = image.astype('float')
    image = scaleImage(image, 100)

    cv2.imshow("Original Image", image)
    cv2.setMouseCallback("Original Image", mousePointsCallbackNORMAL)
    cv2.waitKey(0)

    if (args.debug >= 1):
        print(f"\t{points[0]}")
        print(f"\t{points[1]}")
    return points

def runAStar(image,start,end):
    start = [start[1],start[0]]
    end = [end[1],end[0]]
    # start = (210,44)
    # end = (210,46)
    print(f"Map Size {np.shape(image)}")
    path, visited = aStar(image,start,end)
    for node in path:
        image[node[0]][node[1]] =100
    # print(solved)
    return image

if __name__ == '__main__':
    main()

