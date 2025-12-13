import numpy as np
import time
import copy
import sys

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

diamond = [[2, 1], [3, 0], [3, 2], [4,1]]
letterB = [[2,1], [2,2], [3,1], [3,3],[4,1], [4,2], [5,1], [5,3],[6,1], [6,2]]
baseMatrix = np.zeros((8, 16))
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

def createStringMatrix():
    stringMatrixBase = []
    for i in range(8):
        stringMatrixBase.append([])
        for j in range(16):
            stringMatrixBase[i].append('.')
    return stringMatrixBase

def matrixTestingStrings():
    stringMatrixBase = createStringMatrix()

    stringMatrix = copy.deepcopy(stringMatrixBase)
    flag = False
    # letterMatrix[2][1] = 1
    # letterMatrix[3][0] = 1
    # letterMatrix[3][2] = 1
    # letterMatrix[4][1] = 1
    #print(baseMatrix, end="\r")
    for i in stringMatrix:
        print(i)
    print()
    for i in range(len(stringMatrixBase[0]) + 3):
        #letterMatrix = np.zeros((8, 16))
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

def ledMatrixShow(matrix):
    for i in range(8):
        print(matrix[0+16*i:16+16*i])
    print()

def leftToRight(matrix):
    for i in range(len(matrix)):
        if i > 0:
            matrix[i-1] = '.'
        matrix[i] = '0'
        ledMatrixShow(matrix)
        time.sleep(.1)

def topToBottom(matrix):
    for i in range(len(matrix)):
        if i > 0:
            matrix[((i-1)%8)*16 + (i-1)//8] = '.'
        matrix[(i%8)*16 + i//8] = '0'
        ledMatrixShow(matrix)
        time.sleep(.1)

def matrixOrderConversion():
    ledMatrix = []
    for i in range(128):
        ledMatrix.append('.')
    ledMatrixShow(ledMatrix)
    #leftToRight(ledMatrix)
    topToBottom(ledMatrix)


#newLineTesting()
#matrixTesting()
#matrixTestingStrings()
matrixOrderConversion()

def createMatrixPrint():
    return
