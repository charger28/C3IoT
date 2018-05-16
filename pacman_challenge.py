"""
This program is for the C3IoT FDS technical challenge.
"""

import os
import sys
import numpy
import logging
"""
DEBUG:		Detailed information, typically of interest only when diagnosing problems.
INFO:		Confirmation that things are working as expected.
WARNING:	An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
ERROR:		Due to a more serious problem, the software has not been able to perform some function.
CRITICAL:	A serious error, indicating that the program itself may be unable to continue running.
"""
logging.basicConfig(filename='test.log',level=logging.DEBUG)

input_file = sys.argv[1]

__author__ = "Jeff Beck"


# Read the input file and store the corresponding variables
def getInputValues(file_name):
    try:
        with open(file_name, 'r') as f:
            # Get Board Dimensions
            board_dims = f.readline()
            board_x_dim, board_y_dim = board_dims.split()
            
            # Convert to integer
            board_x_dim = int(board_x_dim)
            board_y_dim = int(board_y_dim)
            logging.debug("Board X Dimension: %s" , {board_x_dim})
            logging.debug("Board Y Dimension: %s" , {board_y_dim})

            # Get Initial X,Y Position
            init_pos = f.readline()
            init_x_pos, init_y_pos = init_pos.split()
            
            # Convert to integer
            init_x_pos = int(init_x_pos)
            init_y_pos = int(init_y_pos)
            logging.debug("Initial X Position: %s" , {init_x_pos})
            logging.debug("Initial Y Position: %s" , {init_y_pos})

            # Get List of Movements
            movements = []
            movements = f.readline()
            logging.debug("Movements: %s" , {movements})

            # Get Wall X,Y Co-ordinates and store in list.
            walls = f.read().splitlines()
            
            #replaces spaces with colons
            walls = [x.replace(' ',':') for x in walls]
            logging.debug("Walls are located at: %s," , {*walls})
            
            return {'board_x_dim':board_x_dim,'board_y_dim':board_y_dim,'init_x_pos':init_x_pos,'init_y_pos':init_y_pos,'movements':movements,'walls':walls}
    # except IOError as e:
    except FileNotFoundError:
        logging.critical("Could not find the file: %s" , {file_name})
    except IOError:
        logging.critical("Could not read the file: %s" , {file_name})

#Calculate proposed movement using current position and new movement
def calcPropMovement(curr_x,curr_y,prop_mov):
    #Create proposed movement location variables
    prop_x = curr_x
    prop_y = curr_y
    
    if prop_mov == 'N':
        logging.debug("Proposed movement is N")
        prop_y = prop_y+1
    elif prop_mov == 'S':
        logging.debug("Proposed movement is S")
        prop_y = prop_y-1
    elif prop_mov == 'E':
        logging.debug("Proposed movement is E")
        prop_x = prop_x+1
    elif prop_mov == 'W':  
        logging.debug("Proposed movement is W")
        prop_x = prop_x-1
        logging.debug("The proposed location is: %s" , {prop_x,prop_y})
    return (prop_x,prop_y)    

#Determine is proposed move is valid.  If valid, return new true.  If not valid, return false
def isMoveValid(input_dict,prop_x,prop_y):
    logging.debug("(isMoveValid) Board X dimension is: %s" , {input_dict['board_x_dim']})
    logging.debug("(isMoveValid) - Proposed X: %s" , {prop_x})
    logging.debug("(isMoveValid) - Proposed Y: %s" , {prop_y})
    
    #create proposed location string variable that will be used to compare against the list of wall locations
    prop_loc_str = str(prop_x) + ":" + str(prop_y)
    logging.debug ("(isMoveValid) Proposed location string variable: %s" , {prop_loc_str})
    
    #check to see if the proposed movement hits a wall
    if any (prop_loc_str in l for l in input_dict['walls']):
        return False
    #check to see if the proposed movement hits a border wall
    elif (prop_x < 0) or (prop_x >= input_dict['board_x_dim']):
        return False
    elif (prop_y < 0) or (prop_y >= input_dict['board_y_dim']):
        return False
    else:
        return True

# Coin collect function that updates the coin collection amount.  This function will also determine if a coin has already been collected in that location
def collectCoin(coin_ct,coin_collect_lst,curr_x_pos, curr_y_pos):
        #create current location string to validate against coin collected list
        logging.debug("Starting coin collection function")
        curr_loc_str = str(curr_x_pos) + ":" + str(curr_y_pos)
        logging.debug("(collectCoin) Current X:Y Pos: %s" , {curr_loc_str})
        
        #check to see if the coin has already been collected from this location
        if curr_loc_str not in coin_collect_lst:
            #update coint_ct
            coin_ct += 1
            logging.debug("(collectCoin) Coin Count is: %s" , {coin_ct})
            #update coin collected list
            coin_collect_lst.append(curr_loc_str)
            return coin_ct
        else:
            return coin_ct

def pacman(input_file):
    """ Use this function to format your input/output arguments. Be sure not change the order of the output arguments.
    Remember that code organization is very important to us, so we encourage the use of helper fuctions and classes as you see fit.

    Input:
        1. input_file (String) = contains the name of a text file you need to read that is in the same directory, includes the ".txt" extension
           (ie. "input.txt")
    Outputs:
        1. final_pos_x (int) = final x location of Pacman
        2. final_pos_y (int) = final y location of Pacman
        3. coins_collected (int) = the number of coins that have been collected by Pacman across all movements
    """
    try:
        # Retrieve variable input file based on the 
        #input_file_name = "input.txt"
        input_variables = getInputValues(input_file)
        #logging.debug("Input Variables Dict: ", input_variables)

        # set initial starting position
        curr_x_pos = input_variables['init_x_pos']
        curr_y_pos = input_variables['init_y_pos']
        #create proposed location string variable that will be used to compare against the list of wall locations
        curr_loc_str = str(curr_x_pos) + ":" + str(curr_y_pos)
        logging.debug("Current X Pos: %s" , {curr_x_pos})
        logging.debug("Current Y Pos: %s" , {curr_y_pos})
        logging.debug("Current XY Pos: %s" , {curr_loc_str})

        #Create coin count variable
        coin_ct = 0
        logging.debug("Coin Count: %s", {coin_ct})
        #Create list to keep track of the locations where the coin has already been collected and initiate with starting position
        coin_collect_lst = []
        coin_collect_lst.append(curr_loc_str)

        #Loop over the Movements (NSEW)
        #clean the Movements list
        movement_lst = input_variables['movements']
        for movement in movement_lst:
            #determine if move is valid
            #logging.debug("Current movement is: ", movement)
            prop_x,prop_y = calcPropMovement(curr_x_pos,curr_y_pos,movement)
            if isMoveValid(input_variables,prop_x,prop_y):
                logging.debug("Move is valid")
                #update current location values
                curr_x_pos = prop_x
                curr_y_pos = prop_y
                logging.debug("Updated X Pos: %s" , {curr_x_pos})
                logging.debug("Updated Y Pos: %s" , {curr_y_pos})
                
                #call collectCoin function to check to see if the coin in that spot has already been collected
                coin_ct = collectCoin(coin_ct,coin_collect_lst, curr_x_pos, curr_y_pos)
                logging.debug("Total Coin Count: %s" , {coin_ct})

            else:
                logging.debug("Move is invalid.  Go to the next movement.")    
            
        # return final_pos_x, final_pos_y, coins_collected
        print(curr_x_pos, curr_y_pos,coin_ct)
    except Exception as e:
       #Default return values if an error occurred
       print(e)
       #print(-1,-1,0)

pacman(input_file)
