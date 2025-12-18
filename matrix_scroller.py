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

diamond = [48, 33, 65, 50]
pixelH = [16, 17, 20, 21, 32, 33, 36, 37, 48, 49, 50, 51, 52, 53, 64, 65, 68, 69, 80, 81, 84, 85, 96, 97, 100, 101]
pixelE = [16, 17, 18, 19, 20, 21, 32, 33, 48, 49, 50, 51, 52, 64, 65, 80, 81, 96, 97, 98, 99, 100, 101]
pixelL = [16, 17, 32, 33, 48, 49, 64, 65, 80, 81, 96, 97, 98, 99, 100, 101]
pixelO = [17, 18, 19, 20, 32, 33, 36, 37, 48, 49, 52, 53, 64, 65, 68, 69, 80, 81, 84, 85, 97, 98, 99, 100]
pixelW = [16, 17, 21, 32, 33, 37, 48, 49, 51, 53, 64, 65, 66, 67, 68, 69, 80, 81, 82, 84, 85, 96, 97, 101]
pixelR = [16, 17, 18, 19, 20, 32, 33, 36, 37, 48, 49, 52, 53, 64, 65, 66, 67, 68, 80, 81, 84, 85, 96, 97, 100, 101]
pixelD = [16, 17, 18, 19, 20, 32, 33, 36, 37, 48, 49, 52, 53, 64, 65, 68, 69, 80, 81, 84, 85, 96, 97, 98, 99, 100]

pixelLetters = {
    "H": pixelH,
    "E": pixelE,
    "L": pixelL,
    "O": pixelO,
    "W": pixelW,
    "R": pixelR,
    "D": pixelD
}

def fastLEDShape(matrix, shape):
    tempMatrix = copy.deepcopy(matrix)
    #for i in range(16 + 7):        # Forwards
    for i in range(15 + 7, -1, -1): # Backwards
        for j in shape:
            if (not ((j % 16)-6 + i < 0)) and ((j % 16) - 6 + i < 16):
                tempMatrix[j - 6 + i] = '0'
        ledMatrixShow(tempMatrix)
        time.sleep(.4)
        tempMatrix = copy.deepcopy(matrix)

'''
This will more than likely be the version I translate to the appropriate language for project
Still requires further development; maybe helper functions to make it cleaner and remove test/debug code

While loop version of the previous fastLEDShape method. The original works for only one character
at a time, while this one works for as many as there are in a list.
'''
def fastLEDShapeWhile(matrix, shapes):
    tempMatrix = copy.deepcopy(matrix)
    # The count is just for testing adding more letters
    count = 0
    testLetter = copy.deepcopy(pixelH)
    testLetter.insert(0, 22)
    testLetter2 = copy.copy(testLetter)
    delFlag = False

    # The first value in each shape list will be a tracker for where to print it in the final matrix
    while len(shapes) > 0:
        for letter in shapes:
            for pixel in range(len(letter) - 1):
                if (not ((letter[pixel + 1] % 16) -6 + letter[0] < 0)) and ((letter[pixel + 1] % 16) - 6 + letter[0] < 16):
                    tempMatrix[letter[pixel + 1] - 6 + letter[0]] = '0'
            letter[0] -= 1
            if letter[0] < 0:
                # I orignally had del remove the character in this comparison, but that caused a bug
                # where it would print an empty matrix even though there was another item, so I'm
                # assuming it causes a break in the for loop for some reason. Maybe this bug won't 
                # happen in the other language.
                delFlag = True
        ledMatrixShow(tempMatrix)
        time.sleep(.4)
        tempMatrix = copy.deepcopy(matrix)
        count += 1
        if count == 7:
            shapes.append(testLetter)
        elif count == 14:
            shapes.append(testLetter2)
        if delFlag:
            del shapes[0]
            delFlag = False

def fastLEDText(matrix, text):
    tempMatrix = copy.deepcopy(matrix)
    tempLetters = []
    count = 0
    delFlag = False
    addFlag = False

    tempLetter = copy.copy(pixelLetters[text[0]])
    tempLetter.insert(0, 22)
    tempLetters.append(tempLetter)

    while len(tempLetters) > 0:
        for letter in tempLetters:
            for pixel in range(len(letter) - 1):
                if (not ((letter[pixel + 1] % 16) -6 + letter[0] < 0)) and ((letter[pixel + 1] % 16) - 6 + letter[0] < 16):
                    tempMatrix[letter[pixel + 1] - 6 + letter[0]] = '0'
            letter[0] -= 1
            if letter[0] < 0:
                delFlag = True
        ledMatrixShow(tempMatrix)
        time.sleep(.4)
        tempMatrix = copy.deepcopy(matrix)
        if delFlag:
            del tempLetters[0]
            delFlag = False
        if len(tempLetters) > 0:
            if tempLetters[-1][0] < 15:
                count += 1
                if (count < len(text) and (text[count] != " ")):
                    tempLetter = copy.copy(pixelLetters[text[count]])
                    tempLetter.insert(0, 22)
                    tempLetters.append(tempLetter)
            elif tempLetters[-1][0] < 14:
                count += 1

# Function for testing conversion methods
def matrixOrderConversion():
    pixelHtest = pixelH
    ledMatrix = []
    convertedMatrix = []
    for i in range(128):
        ledMatrix.append('.')
    convertedMatrix = fastLEDConversion(ledMatrix)
    ledMatrixShow(ledMatrix)
    ledMatrixShow(convertedMatrix) # for visualization
    #fastLEDShape(ledMatrix, pixelH)
    pixelHtest = [x + 22 for x in pixelHtest]
    pixelHtest2 = copy.copy(pixelH)
    pixelHtest2.insert(0, 22)
    #fastLEDShapeWhile(ledMatrix, [pixelHtest2])
    #leftToRight(ledMatrix)
    #topToBottom(ledMatrix)
    fastLEDText(ledMatrix, "HELLO WORLD")

def main():
    #newLineTesting()
    #matrixTesting()
    #matrixTestingStrings()
    matrixOrderConversion()

main()