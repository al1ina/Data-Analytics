import matplotlib.pyplot as plt
import numpy as np
import math


def read_csv(filename, include_headers = True):
    """
    Reads CSV file and returns the contents in the form of a 2D list
   
    Parameters:
        filename (string): name of the csv file with .csv at the end
        include_headers (boolean): option for the function to analyze the CSV file with or without headers
   
    Returns:
        2D array (list): contents in the csv file
   
    You may not assume that the number of columns in each row is the same.
    If the data contains numerical values, the function should return them as floats, not strings. An example is provided below.
    """
    f = open(filename, "r") # Opens the file and reads it
    lines = f.read().splitlines() #  Reads the file and splits it into a list of lines


    data = [line.split(",") for line in lines] # Processes each line of the file splitting it up at each comma
   
    if include_headers == False: # Checks whether the flag, include_headers is false
        data = data[1:] # Removes the first row, the header


    for row in range(len(data)): # Iterates through each row of data
        for column in range(len(data[row])): # Iterates through each column
            try: # This is a function that "tries" to convert the value to a float, if it can't it jumps to the except
                data[row][column] = float(data[row][column])
            except ValueError: # The value is not a float
                pass # Keeps the value as a string i.e. does nothing


    return data # Returns the processed data as a 2D list


def write_csv(filename, data, overwrite):
    """
    A function that overwrites or appends data to an existing file.


    Parameters:
        filename (string): name of the csv file with .csv at the end
        data (2D list): contains the data that will be written to csv file
        overwrite (boolean): indicates whether the function will overwrite or append to an existing file
    """
    if overwrite == True:
        parameter = "w" # Sets the paramter to "w" meaning that the user will overwrite the contents of the file
   
    else:
        parameter = "a" # Sets the parameter to "a" meaning that the user will add on to the end of the file


    with open(filename, parameter, newline = "") as file: # Opens the file with the parameter making sure no extra white spaces are added
        for row in data: # Iterates through each row
            line = ','.join(str(cell) for cell in row) # Iterates through each column in row
            file.write(line + "\n")






