# 15112-TP
## Project Description:
This project is a game of Ultimate Tic Tac Toe, where the winner of each spot on the board is determined by the outcome of a "sub-game." This version has a twist, in that each sub-game is a game of 3D Tic Tac Toe, where pieces can be played in the vertical, horizontal, or normal axes. Players alternate picking the location of the sub-game, and the player who picks the sub-game gets to go first for that sub-game. Theres are both single-player and two-player modes, where the former involves playing against the computer, and the latter is between two individuals.

## Running the game:
This program is coded using Python, so being able to run Python scripts is required.

### If you don't have Python 3 installed or are unsure:
Run the following in your Terminal (Mac):

    python3 --verison

If this is not 3.6.x or above, you will need to install the latest version by going to https://www.python.org/downloads/
Once this is installed, you are all set!

Download and unzip the zip file from this page, as this is the final version. Ensure that the TP3.py and the cmu_112_graphics.py files are both present (this should be the case by default). You may now either open and run TP3.py from an editor, or you can use Terminal (MacOS).

To use Terminal, right click on the unzipped folder and select "New Terminal at Folder", then run the following line:

    python3 TP3.py

## Code Libraries:
TP3.py uses the tkinter module, which is called using cmu_112_graphics.py, so no extra steps are necessary to run the game.

## Shortcut Commands:
Hitting the "r" key while in a 3D sub-game will reset the 3D game board, without returning to the primary 2D board.
