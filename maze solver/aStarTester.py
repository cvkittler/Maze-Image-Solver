from aStarOptimized import aStar
import numpy as np
from PIL import Image
import unittest

# Image.fromarray(np.uint8(image)).save("./unitTestingMazes/a.png")



class aStarTests(unittest.TestCase):
    def testNoPath(self): # test method names begin with 'test'
        image = np.zeros((11,11))
        image[0,5]= 255 
        image[10,5]= 255
        for j in range(1,10,2):
            for i in range(9):
                image[j,i+1] = 255
        # Image.fromarray(np.uint8(image)).save("./unitTestingMazes/a.png")
        self.assertEqual(aStar(image,[0,5],[10,5])[1], None)

    def testStraitPath(self):
        image = np.zeros((11,11))
        for j in range(11):
            image[j,5] = 255
        # Image.fromarray(np.uint8(image)).save("./unitTestingMazes/b.png")
        self.assertEqual(aStar(image,[0,5],[10,5]), ([(10, 5), (9, 5), (8, 5), (7, 5), (6, 5), (5, 5), (4, 5), (3, 5), (2, 5), (1, 5), (0, 5)], [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5)]))

    def testBackTrack(self):
        image = np.ones((11,11))*255
        image[5,5]=0
        image[5,4]=0
        image[5,6]=0
        image[4,4]=0
        image[4,6]=0
        image[3,4]=0
        image[3,6]=0
        path, visited = aStar(image,[0,5],[10,5])
        for id,node in enumerate(path):
            image[node[0]][node[1]] =50 +id* 10
        # for id,visited in enumerate(path):
        #     image[node[0]][node[1]] =100
        Image.fromarray(np.uint8(image)).save("./unitTestingMazes/c.png")
        self.assertNotEqual(path, visited)

if __name__ == '__main__':
    unittest.main()