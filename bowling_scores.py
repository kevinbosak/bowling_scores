#!/usr/bin/env python


MAX_FRAMES = 10


class InvalidRoll(Exception):
    pass


class BowlingFrame:
    def __init__(self):
        self.score = None
        self.rolls = []
        self.done_rolling = False

    def add_roll(self, roll):
        """ Takes a roll and calculates the frame's score (if possible) and
            checks whether this frame is done rolling
        """

        self.rolls.append(roll)

        # check for open frame, strike, and spare
        if (len(self.rolls) == 2 and sum(self.rolls) < 10) or \
                (len(self.rolls) == 3 and (self.rolls[0] == 10 or
                                           sum(self.rolls[:2]) == 10)):
            self.score = sum(self.rolls)

        elif len(self.rolls) == 1 and roll != 10:
            # use the first roll of an unresolved frame for score if it's not a
            # strike
            self.score = roll

        else:
            self.score = None

        if len(self.rolls) == 2 or roll == 10:
            self.done_rolling = True


class Bowler:
    """ This class represent a bowler playing a single game. It keeps track of
        the bowler's rolls and calculates the score after each roll.
    """

    def __init__(self, bowler_name='bowler'):
        self.bowler_name = bowler_name
        self.current_frame_id = 1
        self.frames = [BowlingFrame() for i in range(MAX_FRAMES)]

    @property
    def score(self):
        score = 0
        for frame in self.frames:
            if frame.score:
                score += frame.score
        return score

    def is_done_bowling(self):
        """ Returns a boolean value to tell whether there are any more
            rolls or frames remaining.
        """
        if self.current_frame_id == MAX_FRAMES and \
                self.frames[MAX_FRAMES-1].score is not None:
            return True

        return False

    def add_roll(self, value):
        """ Takes either an integer value for the number of pins knocked down
            on th current roll and adjusts the current frame's remaining pins
            and bowler's score.
        """

        # validation
        if self.is_done_bowling():
            raise InvalidRoll("The game is over.")
        elif not isinstance(value, int):
            raise TypeError("Only integers are accepted for rolls.")
        elif value < 0 or value > 10:
            raise ValueError("Roll values must be between 0 - 10, inclusive.")

        # Add to any prior unresolved frames first, then to current frame
        for i, frame in enumerate(self.frames):
            if frame.score is not None:
                continue
            frame.add_roll(value)
            if i + 1 == self.current_frame_id:
                if frame.done_rolling and self.current_frame_id != MAX_FRAMES:
                    self.current_frame_id += 1

    def get_score(self):
        """ Returns the bowler's current score.  Note that the current score
            may not take into account spares and strikes that are not fully
            resolved
        """
        score = 0
        for frame in self.frames:
            if frame.score:
                score += frame.score
        return score


if __name__ == '__main__':
    print("""Bowling Scores:
    This program will prompt you for the number of pins you knock down
    for each shot on each frame.  Enter the number of pins as an integer.
    You may also use 'X' for strikes or '/' for spares.
    """)

    bowler = Bowler()
    while (not bowler.is_done_bowling()):
        score = bowler.get_score()
        print("Your current score is {score}")

        frame, roll = bowler.get_next_roll()
        pins = input(f"Enter pins knocked down for frame {frame}, roll {roll}")
        try:
            bowler.add_roll(pins)
        except ValueError:
            print("Invalid value entered, try again.")
            continue

    score = bowler.get_score()
    if score == 300:
        print("Perfect game!!")
    else:
        print("Your total score is {score}.")
