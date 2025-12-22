#include <iostream>
#include <vector>
#include <string>
#include <span>
#include <thread>
#include <chrono>
#include <unordered_map>
#include <deque>

using namespace std;

static vector<int> pixelH = {16, 17, 20, 21, 32, 33, 36, 37, 48, 49, 50, 51, 52, 53, 64, 65, 68, 69, 80, 81, 84, 85, 96, 97, 100, 101};
static vector<int> pixelE = {16, 17, 18, 19, 20, 21, 32, 33, 48, 49, 50, 51, 52, 64, 65, 80, 81, 96, 97, 98, 99, 100, 101};
static vector<int> pixelL = {16, 17, 32, 33, 48, 49, 64, 65, 80, 81, 96, 97, 98, 99, 100, 101};
static vector<int> pixelO = {17, 18, 19, 20, 32, 33, 36, 37, 48, 49, 52, 53, 64, 65, 68, 69, 80, 81, 84, 85, 97, 98, 99, 100};
static vector<int> pixelW = {16, 17, 21, 32, 33, 37, 48, 49, 51, 53, 64, 65, 66, 67, 68, 69, 80, 81, 82, 84, 85, 96, 97, 101};
static vector<int> pixelR = {16, 17, 18, 19, 20, 32, 33, 36, 37, 48, 49, 52, 53, 64, 65, 66, 67, 68, 80, 81, 84, 85, 96, 97, 100, 101};
static vector<int> pixelD = {16, 17, 18, 19, 20, 32, 33, 36, 37, 48, 49, 52, 53, 64, 65, 68, 69, 80, 81, 84, 85, 96, 97, 98, 99, 100};

static unordered_map<char, vector<int>> letterDict = {
  { 'H', pixelH}, { 'E', pixelE}, { 'L', pixelL}, { 'O', pixelO}, { 'W', pixelW}, { 'R', pixelR},
  { 'D', pixelD} 
};

void displayMatrix(vector<string> matrix)
{
    for (int i = 0; i < matrix.size(); i++)
    {
        if (i % 16 == 0)
        {
            cout << endl;
        }
        cout << matrix.at(i) << " ";
    }
    cout << endl;
    this_thread::sleep_for(chrono::milliseconds(100));
}

void modifyMatrix(vector<string> matrix, string displayText) 
{
    vector<string> tmpMatrix = matrix;
    deque<vector<int>> lettersToDisplay;
    vector<int> tmpLetter;
    bool delFlag = false;
    int letterPos = 0;
    int letterToAdd = 0;
    span<char> displayTextExpanded(displayText);

    tmpLetter = letterDict.at(displayTextExpanded[letterToAdd]);
    tmpLetter.push_back(22);
    lettersToDisplay.push_back(tmpLetter);
    
    while ( lettersToDisplay.empty() == 0 )
    {
        for (vector<int> letter : lettersToDisplay)
        {
            for (int pixel = 0; pixel < letter.size() - 1; pixel ++)
            {
                if ((!((letter.at(pixel) % 16) - 6 + letter.back() < 0)) && ((letter.at(pixel) % 16) - 6 + letter.back() < 16))
                {
                    tmpMatrix.at(letter.at(pixel) - 6 + letter.back()) = '0';
                }
            }
            lettersToDisplay.at(letterPos).back() --;
            letterPos ++;
        }

        letterPos = 0;
        if (lettersToDisplay.front().back() < 0) { delFlag = true; }
        displayMatrix(tmpMatrix);
        tmpMatrix = matrix;
        if (delFlag)
        {
            delFlag = false;
            lettersToDisplay.pop_front();
        }
        if (lettersToDisplay.empty() == 0)
        {
            if (lettersToDisplay.back().back() < 15)
            {
                letterToAdd ++;
                if (letterToAdd < displayTextExpanded.size() && displayTextExpanded[letterToAdd] != ' ')
                {
                    tmpLetter = letterDict.at(displayTextExpanded[letterToAdd]);
                    tmpLetter.push_back(22);
                    lettersToDisplay.push_back(tmpLetter);
                }
            }
        }
    }
}

int main()
{
    vector<string> ledMatrix;
    ledMatrix.assign(128, ".");

    modifyMatrix(ledMatrix, "HELLO WORLD");
}
