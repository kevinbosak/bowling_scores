# Bowling Scores
A simple example library and program to calculate bowling scores using Python 3.
You may run 'bowling_scores.py' directly, or include its "Bowler" class
to use in your own programs.

## Input
This script will prompt the user for input from the command line.  It will only
accept integer values as well as '/' or 'X' for strikes and spares, accordingly.

## Explanation
Bowling scores are calculated as follows:

### Strike
If you knock down all 10 pins in the first shot of a frame, you get a strike.
A strike earns 10 points plus the sum of your next two shots.

### Spare
If you knock down all 10 pins using both shots of a frame, you get a spare.
A spare earns 10 points plus the sum of your next one-shot.

### Open Frame
If you do not knock down all 10 pins using both shots of your frame (9 or fewer pins knocked down), you have an open frame.
An open frame only earns the number of pins knocked down.

### The 10th Frame

* If you roll a strike in the first shot of the 10th frame, you get 2 more shots.
* If you roll a spare in the first two shots of the 10th frame, you get 1 more shot.
* If you leave the 10th frame open after two shots, the game is over and you do not get an additional shot.
* The score for the 10th frame is the total number of pins knocked down in the 10th frame.
