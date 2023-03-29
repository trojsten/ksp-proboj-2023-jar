from unittest import TestCase

from libs.geometry import *


class TestSegment(TestCase):
    def test_collides(self):
        self.assertTrue(Segment.collides(Segment(XY(0, 0), XY(0, 0)), 1,
                                         Segment(XY(1, 0), XY(1, 0)), 1))

        self.assertFalse(Segment.collides(Segment(XY(0, 0), XY(0, 0)), 1,
                                          Segment(XY(10, 10), XY(10, 10)), 1))
        
        self.assertTrue(Segment.collides(Segment(XY(0, 0), XY(10, 0)), 1,
                                         Segment(XY(5, 0), XY(5, 0)), 1))
        
        self.assertTrue(Segment.collides(Segment(XY(0, 0), XY(1, 0)), 1,
                                         Segment(XY(1, 0), XY(0, 0)), 1))
        
        self.assertTrue(Segment.collides(Segment(XY(0, 0), XY(1, 0)), 0,
                                         Segment(XY(1, 0), XY(0, 0)), 0))
        
        self.assertTrue(Segment.collides(Segment(XY(0, 0), XY(1, 0)), 1,
                                         Segment(XY(1, 1), XY(0, 1)), 1))

        self.assertTrue(Segment.collides(Segment(XY(0, 0), XY(1, 0)), 0.5,
                                         Segment(XY(1, 1), XY(0, 1)), 0.5))

        self.assertFalse(Segment.collides(Segment(XY(0, 0), XY(1, 0)), 0.5,
                                          Segment(XY(1, 1), XY(0, 1)), 0.49))

        self.assertFalse(Segment.collides(Segment(XY(0, 0), XY(0, 100)), 1,
                                          Segment(XY(-100, 100), XY(100, 100)), 1))

        self.assertFalse(Segment.collides(Segment(XY(0, 0), XY(0, 100)), 1,
                                          Segment(XY(-100, 0), XY(100, 0)), 1))



