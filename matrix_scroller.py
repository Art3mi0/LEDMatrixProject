'''
Project goal: Display weather data for fishing on a LED Matrix
Parameters: - Text scrolls from right to left
            - Pull data either from a known free weather data api or something or obtain data 
              in some way from target site and process data from site accordingly

Testing on an Arduino uno and ws2812b rgb led matrix. Will eventually use an esp32 for wifi
capability.

Current Problems:   - Arduino limited in memory. Using fastLED library and just the 256 led array
                      is almost half the memory. Need to keep stored variables to a minimum.
                    - fastLED array led display is ordered from top to bottom. Python 2D arrays
                      are ordered from left to right. Need to develop a conversion.
'''

import numpy as np
import time
import copy
import sys

'''
Attempted to display matrix in multiple lines on terminal to simulate led matrix but did not work
and only thing that reliably works is single line replacement. Opted instead to just print the
matrix each time but resize the window to only show 1 matrix to give the illusion that it is
a single matrix updating
'''
# def overwrite_multiple_lines(lines_to_overwrite, new_content):
#     # Move cursor up by the number of lines to overwrite
#     sys.stdout.write(f"\033[{lines_to_overwrite}A")
#     for line in new_content:
#         sys.stdout.write("\033[K")  # Clear the current line
#         sys.stdout.write(line + "\n")
#     sys.stdout.flush()

def newLineTesting():
    print("test\ntest2")
    time.sleep(1)
    #overwrite_multiple_lines(2, ["bozo", "deez"])

###

'''
Attempting scrolling text at this point.
'''

# Will need to make a dictionary at some point for each letter, but as a concept, these do the job
diamond = [[2, 1], [3, 0], [3, 2], [4,1]]
letterB = [[2,1], [2,2], [3,1], [3,3],[4,1], [4,2], [5,1], [5,3],[6,1], [6,2]]\


baseMatrix = np.zeros((8, 16))

# This was an attempt with a regular matrix of ints, but it is a little hard to see for simulating
def matrixTesting():
    letterMatrix = np.zeros((8, 16))
    falg = False
    # letterMatrix[2][1] = 1
    # letterMatrix[3][0] = 1
    # letterMatrix[3][2] = 1
    # letterMatrix[4][1] = 1
    #print(baseMatrix, end="\r")
    print(baseMatrix)
    print()
    for i in range(len(baseMatrix[0]) + 3):
        #letterMatrix = np.zeros((8, 16))
        letterMatrix = baseMatrix.copy()
        for j in letterB:
            flag = False
            x = j[1] - 2 + i
            if x < 0 or x > 15:
                x = 0
                flag = True
            if not flag:
                letterMatrix[j[0]][x] = 1
        time.sleep(.35)
        print(letterMatrix)
        print()

# Helper function for creating string matrix
def createStringMatrix():
    stringMatrixBase = []
    for i in range(8):
        stringMatrixBase.append([])
        for j in range(16):
            stringMatrixBase[i].append('.')
    return stringMatrixBase

# A copy of my first attempt without numpy using strings
def matrixTestingStrings():
    stringMatrixBase = createStringMatrix()
    stringMatrix = copy.deepcopy(stringMatrixBase) # Without deepcopy it makes a reference to the original resulting in the original being modified
    flag = False

    for i in stringMatrix:
        print(i)
    print()
    for i in range(len(stringMatrixBase[0]) + 3):
        stringMatrix = copy.deepcopy(stringMatrixBase)
        for j in letterB:
            flag = False
            x = j[1] - 2 + i
            if x < 0 or x > 15:
                x = '.'
                flag = True
            if not flag:
                stringMatrix[j[0]][x] = '0'
        time.sleep(.35)
        for i in stringMatrix:
            print(i)
        print()

'''
fastLED array conversion
'''

# Helper function for displaying the current matrix
def ledMatrixShow(matrix):
    for i in range(8):
        print(matrix[0+16*i:16+16*i])
    print()

# Function for displaying a moving *light* from left to right in python
def leftToRight(matrix):
    for i in range(len(matrix)):
        if i > 0:
            matrix[i-1] = '.'
        matrix[i] = '0'
        ledMatrixShow(matrix)
        time.sleep(.1)

# Function for displaying a moving *light* from top to bottom in python
# Using only math to avoid creating variables
def topToBottom(matrix):
    for i in range(len(matrix)):
        if i > 0:
            matrix[((i-1)%8)*16 + (i-1)//8] = '.'
        matrix[(i%8)*16 + i//8] = '0'
        ledMatrixShow(matrix)
        time.sleep(.1)

def fastLEDConversion(matrix):
    convertedMatrix = copy.deepcopy(matrix)
    for i in range(len(convertedMatrix)):
        convertedMatrix[(i%8)*16 + i//8] = str(i)
    return convertedMatrix

def fastLEDShape(matrix):
    tempMatrix = copy.deepcopy(matrix)
    diamond = [48, 33, 65, 50]
    for i in range(16):
        for j in diamond:
            tempMatrix[j + i] = '0'
        ledMatrixShow(tempMatrix)
        time.sleep(.4)
        tempMatrix = copy.deepcopy(matrix)

# Function for testing conversion methods
def matrixOrderConversion():
    ledMatrix = []
    convertedMatrix = []
    for i in range(128):
        ledMatrix.append('.')
    convertedMatrix = fastLEDConversion(ledMatrix)
    ledMatrixShow(ledMatrix)
    ledMatrixShow(convertedMatrix) # for visualization
    #fastLEDShape(ledMatrix)
    #leftToRight(ledMatrix)
    #topToBottom(ledMatrix)

def main():
    #newLineTesting()
    #matrixTesting()
    #matrixTestingStrings()
    matrixOrderConversion()

main()