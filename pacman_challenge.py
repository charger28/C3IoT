"""
This program is for the C3IoT FDS technical challenge.
"""
__author__ = "Jeff Beck"

import os
import sys
import numpy
import logging
from pathlib import Path

#Set the logging properties.
logging.basicConfig(filename="test.log",level=logging.DEBUG)

#Read the file name from the command prompt.
input_file = sys.argv[1]


#Read the input file and store the corresponding variables.
def get_input_values(file_name):
    try:
        with open(file_name, "r") as f:
            #Get Board Dimensions.
            board_dims = f.readline()
            board_x_dim, board_y_dim = board_dims.split()
            #Convert to integer.
            board_x_dim = int(board_x_dim)
            board_y_dim = int(board_y_dim)
            logging.debug("Board X Dimension: %s" , {board_x_dim})
            logging.debug("Board Y Dimension: %s" , {board_y_dim})

            #Get Initial X,Y Position.
            init_pos = f.readline()
            init_x_pos, init_y_pos = init_pos.split()
            #Convert to integer
            init_x_pos = int(init_x_pos)
            init_y_pos = int(init_y_pos)
            logging.debug("Initial X Position: %s" , {init_x_pos})
            logging.debug("Initial Y Position: %s" , {init_y_pos})

            #Get List of Movements.
            movements = []
            movements = f.readline()
            logging.debug("Movements: %s" , {movements})

            #Get interior Wall X,Y Co-ordinates and store in list.
            walls = f.read().splitlines()
            #Replaces spaces with colons.
            walls = [x.replace(" ",":") for x in walls]
            logging.debug("Walls are located at: %s," , {*walls})
            
            #Return variables in a dictionary.
            return {"board_x_dim":board_x_dim,"board_y_dim":board_y_dim,"init_x_pos":init_x_pos,"init_y_pos":init_y_pos,"movements":movements,"walls":walls}
    #Except IOError as e:
    except FileNotFoundError:
        logging.critical("Could not find the file: %s" , {file_name})
    except IOError:
        logging.critical("Could not read the file: %s" , {file_name})


#Calculate the "proposed movement" using current position and cardinal movement.
def calc_Prop_Movement(curr_x,curr_y,prop_mov):
    #Create "proposed movement" location variables.
    prop_x = curr_x
    prop_y = curr_y
    
    if prop_mov == "N":
        #Increase Y coordinate location by 1.
        logging.debug("Proposed movement is N")
        prop_y = prop_y+1
    elif prop_mov == "S":
        #Decrease Y coordinate location by 1.
        logging.debug("Proposed movement is S")
        prop_y = prop_y-1
    elif prop_mov == "E":
        #Increase X coordinate location by 1.
        logging.debug("Proposed movement is E")
        prop_x = prop_x+1
    elif prop_mov == "W":  
        #Decrease X coordinate location by 1.
        logging.debug("Proposed movement is W")
        prop_x = prop_x-1
        logging.debug("The proposed location is: %s" , {prop_x,prop_y})
    return (prop_x,prop_y)    


#Determine if the proposed move is valid.  The function will check for interior walls and boundaries.
#If valid, return true.  If not valid, return false.
def isMoveValid(input_dict,prop_x,prop_y):
    logging.debug("(isMoveValid) Board X dimension is: %s" , {input_dict["board_x_dim"]})
    logging.debug("(isMoveValid) - Proposed X: %s" , {prop_x})
    logging.debug("(isMoveValid) - Proposed Y: %s" , {prop_y})
    
    #Create proposed location string variable that will be used to compare against the list of interior wall locations.
    prop_loc_str = str(prop_x) + ":" + str(prop_y)
    logging.debug ("(isMoveValid) Proposed location string variable: %s" , {prop_loc_str})
    
    #Check to see if the proposed movement hits an interior wall.
    if any (prop_loc_str in l for l in input_dict["walls"]):
        return False
    #Check to see if the proposed movement hits a border wall.
    elif (prop_x < 0) or (prop_x >= input_dict["board_x_dim"]):
        return False
    elif (prop_y < 0) or (prop_y >= input_dict["board_y_dim"]):
        return False
    else:
        return True


#Coin collect function that updates the total coin collection amount.
#This function will also determine if a coin has previously been collected in that location.
def collect_coin(coin_ct,coin_collect_lst,curr_x_pos, curr_y_pos):
        #Create current location string to validate against coin collected list.
        logging.debug("Starting coin collection function")
        curr_loc_str = str(curr_x_pos) + ":" + str(curr_y_pos)
        logging.debug("(collect_coin) Current X:Y Pos: %s" , {curr_loc_str})
        
        #Check to see if the coin has already been collected from this location.
        if curr_loc_str not in coin_collect_lst:
            #Coin has not previously been collected, update coint_ct.
            coin_ct += 1
            logging.debug("(collect_coin) Coin Count is: %s" , {coin_ct})
            #Add the current location to the coin collected list.
            coin_collect_lst.append(curr_loc_str)
            return coin_ct
        else:
            return coin_ct


#This function formats the input/output arguments.
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
        #Retrieve variables from the input file.
        input_variables = get_input_values(input_file)

        #Set initial starting position.
        curr_x_pos = input_variables["init_x_pos"]
        curr_y_pos = input_variables["init_y_pos"]
        
        #Create "proposed location" variable that will be used to compare against the list of wall locations.
        curr_loc_str = str(curr_x_pos) + ":" + str(curr_y_pos)
        logging.debug("Current XY Pos: %s" , {curr_loc_str})

        #Create coin count variable
        coin_ct = 0
        
        #Create a list to keep track of the locations where the coin has already been collected and initiate with starting position.
        coin_collect_lst = []
        coin_collect_lst.append(curr_loc_str)

        #Loop over the Movements (NSEW).
        #Clean the Movements list.
        movement_lst = input_variables["movements"]
        for movement in movement_lst:
            #Call function to determine if the move is valid.
            prop_x,prop_y = calc_Prop_Movement(curr_x_pos,curr_y_pos,movement)
            if isMoveValid(input_variables,prop_x,prop_y):
                logging.debug("Move is valid")
                #Update current location values.
                curr_x_pos = prop_x
                curr_y_pos = prop_y
                logging.debug("Updated X Pos: %s" , {curr_x_pos})
                logging.debug("Updated Y Pos: %s" , {curr_y_pos})
                
                #Call collect_coin function to check to see if the coin in that spot has already been collected.
                coin_ct = collect_coin(coin_ct,coin_collect_lst, curr_x_pos, curr_y_pos)
                logging.debug("Total Coin Count: %s" , {coin_ct})

            else:
                logging.debug("Move is invalid.  Go to the next movement.")    
            
        #Return final_pos_x, final_pos_y, coins_collected.
        print("%s, %s, %s" % (curr_x_pos, curr_y_pos,coin_ct))
    except Exception:
       #Default return values if an error occurred.
       print("-1, -1, 0")

pacman(input_file)
