#This unit test code will test the 'calcPropMovement' function in pacman.py.  This function changes the x,y position based
#upon the cardinal direction

import unittest
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from pacman_challenge import calcPropMovement

class TestPacmanChallenge(unittest.TestCase):
   
    def test_calcPropMovement(self):
        x_pos,y_pos = calcPropMovement(1,1,'N')
        self.assertEqual(x_pos,1)
        self.assertEqual(y_pos,2)

        x_pos,y_pos = calcPropMovement(1,1,'S')
        self.assertEqual(x_pos,1)
        self.assertEqual(y_pos,0)       

        x_pos,y_pos = calcPropMovement(1,1,'E')
        self.assertEqual(x_pos,2)
        self.assertEqual(y_pos,1)

        x_pos,y_pos = calcPropMovement(1,1,'W')
        self.assertEqual(x_pos,0)
        self.assertEqual(y_pos,1)

if __name__ == '__main__':
    unittest.main()