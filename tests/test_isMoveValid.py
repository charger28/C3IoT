#This unit test code will test the 'isMoveValid' function in pacman.py.  This function checks
#if a proposed move will either hit a wall or a boundary.  The function returns a TRUE or FALSE

import unittest
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from pacman_challenge import isMoveValid

class TestPacmanChallenge(unittest.TestCase):
   
    def test_isMoveValid(self):
        
        # True tests
        testWalls = {'1:1'}
        prop_x,prop_y = 0,1
        self.assertTrue(isMoveValid(testWalls,prop_x,prop_y))

        #False tests for wall conflicts
        testWalls = {'1:1'}
        prop_x,prop_y = 1,1
        self.assertTrue(isMoveValid(testWalls,prop_x,prop_y))

        #False tests for border conflicts
        testWalls = {'0:1'}
        prop_x,prop_y = -1,1
        self.assertTrue(isMoveValid(testWalls,prop_x,prop_y))

if __name__ == '__main__':
    unittest.main()