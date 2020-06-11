import unittest
from unittest.mock import patch

from bowling_scores import BowlingFrame, Bowler, InvalidRoll


class TestBowlingFrame(unittest.TestCase):

    def test_add_roll__open(self):
        frame = BowlingFrame()
        frame.add_roll(5)

        self.assertEqual(frame.rolls, [5])
        self.assertEqual(frame.score, 5)
        self.assertFalse(frame.done_rolling)

        frame.add_roll(3)

        self.assertEqual(frame.rolls, [5, 3])
        self.assertEqual(frame.score, 8)
        self.assertTrue(frame.done_rolling)

    def test_add_roll__spare(self):
        frame = BowlingFrame()
        frame.add_roll(4)

        self.assertEqual(frame.rolls, [4])
        self.assertEqual(frame.score, 4)
        self.assertFalse(frame.done_rolling)

        frame.add_roll(6)

        self.assertEqual(frame.rolls, [4, 6])
        self.assertIsNone(frame.score)
        self.assertTrue(frame.done_rolling)

        frame.add_roll(8)

        self.assertEqual(frame.rolls, [4, 6, 8])
        self.assertEqual(frame.score, 18)
        self.assertTrue(frame.done_rolling)

    def test_add_roll__strike(self):
        frame = BowlingFrame()
        frame.add_roll(10)

        self.assertEqual(frame.rolls, [10])
        self.assertIsNone(frame.score)
        self.assertTrue(frame.done_rolling)

        frame.add_roll(3)

        self.assertEqual(frame.rolls, [10, 3])
        self.assertIsNone(frame.score)
        self.assertTrue(frame.done_rolling)

        frame.add_roll(4)

        self.assertEqual(frame.rolls, [10, 3, 4])
        self.assertEqual(frame.score, 17)
        self.assertTrue(frame.done_rolling)


class TestBowler(unittest.TestCase):

    def setUp(self):
        self.bowler = Bowler('test')

    def test_add_roll_exceptions(self):
        self.assertRaises(TypeError, self.bowler.add_roll, 'fail')
        self.assertRaises(ValueError, self.bowler.add_roll, 11)
        #with patch('__main__.Bowler.is_done_bowling', return_value=True):
        with patch('bowling_scores.Bowler.is_done_bowling', return_value=True):
            self.assertRaises(InvalidRoll, self.bowler.add_roll, 10)

    def test_add_roll(self):
        self.assertEqual(self.bowler.current_frame_id, 1)

        # Frame 1: open frame
        self.bowler.add_roll(5)
        self.assertEqual(self.bowler.frames[0].rolls, [5])

        self.bowler.add_roll(3)
        self.assertEqual(self.bowler.frames[0].rolls, [5, 3])
        self.assertEqual(self.bowler.current_frame_id, 2)

        # Frame 2: strike
        self.bowler.add_roll(10)
        self.assertEqual(self.bowler.frames[1].rolls, [10])
        self.assertFalse(self.bowler.frames[1].is_resolved)
        self.assertEqual(self.bowler.current_frame_id, 3)

        # Frame 3: spare, resolving strike
        self.bowler.add_roll(6)
        self.assertEqual(self.bowler.frames[1].rolls, [10, 6])
        self.assertEqual(self.bowler.frames[2].rolls, [6])
        self.assertFalse(self.bowler.frames[1].is_resolved)
        self.assertFalse(self.bowler.frames[2].is_resolved)
        self.assertEqual(self.bowler.current_frame_id, 3)

        self.bowler.add_roll(4)
        self.assertEqual(self.bowler.frames[1].rolls, [10, 6, 4])
        self.assertEqual(self.bowler.frames[2].rolls, [6, 4])
        self.assertEqual(self.bowler.current_frame_id, 4)

        self.assertTrue(self.bowler.frames[1].is_resolved)
        self.assertFalse(self.bowler.frames[2].is_resolved)

        # Frame 4: resolving the spare
        self.bowler.add_roll(8)
        self.assertEqual(self.bowler.frames[2].rolls, [6, 4, 8])
        self.assertTrue(self.bowler.frames[2].is_resolved)
        self.assertEqual(self.bowler.current_frame_id, 4)

        # Frame 4: catching cheating
        self.assertRaises(InvalidRoll, self.bowler.add_roll, 3)


if __name__ == '__main__':
    unittest.main()
