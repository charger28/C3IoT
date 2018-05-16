#This unit test code will test the 'is_move_valid' function in pacman.py.  This function checks
#if a proposed move will either hit a wall or a boundary.  The function returns a TRUE or FALSE

import unittest
import sys, os
from pacman_challenge import is_move_valid

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

class TestPacmanChallenge(unittest.TestCase):
   
    def test_is_move_valid(self):
        
        # True tests
        testWalls = {'1:1'}
        prop_x,prop_y = 0,1
        self.assertTrue(is_move_valid(testWalls,prop_x,prop_y))

        #False tests for wall conflicts
        testWalls = {'1:1'}
        prop_x,prop_y = 1,1
        self.assertTrue(is_move_valid(testWalls,prop_x,prop_y))

        #False tests for border conflicts
        testWalls = {'0:1'}
        prop_x,prop_y = -1,1
        self.assertTrue(is_move_valid(testWalls,prop_x,prop_y))

if __name__ == '__main__':
    unittest.main()