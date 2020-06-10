#!/usr/bin/env python


class BowlingScores(object):
    def new(self):
        pass

    def done_bowling(self):
        pass

    def add_roll(self):
        pass

    def get_score(self):
        pass


if __name__ == '__main__':
    print("""Bowling Scores:
    This program will prompt you for the number of pins you knock down
    for each shot on each frame.  Enter the number of pins as an integer.
    You may also use 'X' for strikes or '/' for spares.
    """)

    bowler = BowlingScores()
    while (not bowler.done_bowling()):
        score = bowler.get_score()
        print("Your current score is {score}")

        frame, roll = bowler.get_next_roll()
        pins = input(f"Enter pins knocked down for frame {frame}, roll {roll}")
        try:
            bowler.add_roll(pins)
        except ValueError:
            print("Invalid value entered, try again.")
            continue

    print("Your total score is {score}")
