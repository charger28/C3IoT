#This unit test code will test the 'calc_prop_movement' function in pacman.py.  This function changes the x,y position based
#upon the cardinal direction

import unittest
import sys, os
from pacman_challenge import calc_prop_movement

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

class TestPacmanChallenge(unittest.TestCase):
   
    def test_calc_prop_movement(self):
        x_pos,y_pos = calc_prop_movement(1,1,'N')
        self.assertEqual(x_pos,1)
        self.assertEqual(y_pos,2)

        x_pos,y_pos = calc_prop_movement(1,1,'S')
        self.assertEqual(x_pos,1)
        self.assertEqual(y_pos,0)       

        x_pos,y_pos = calc_prop_movement(1,1,'E')
        self.assertEqual(x_pos,2)
        self.assertEqual(y_pos,1)

        x_pos,y_pos = calc_prop_movement(1,1,'W')
        self.assertEqual(x_pos,0)
        self.assertEqual(y_pos,1)

if __name__ == '__main__':
    unittest.main()