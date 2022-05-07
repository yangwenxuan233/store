import unittest
from Calc import Calc


class TestCalc_sub(unittest.TestCase):

    def testSub1(self):
        a = 2
        b = 3
        c = -1
        calc = Calc()
        dif = calc.sub(a, b)
        self.assertEqual(c, dif)

    def testSub2(self):
        a = 2
        b = -3
        c = -5
        calc = Calc()
        dif = calc.sub(a, b)
        self.assertEqual(c, dif)

    def testSub3(self):
        a = -2
        b = 3
        c = -5
        calc = Calc()
        dif = calc.sub(a, b)
        self.assertEqual(c, dif)

    def testSub4(self):
        a = -2
        b = -3
        c = 1
        calc = Calc()
        dif = calc.sub(a, b)
        self.assertEqual(c, dif)

    def testSub(self):
        a = 2
        b = 3
        c = -1
        calc = Calc()
        dif = calc.sub(a, b)
        self.assertEqual(c, dif)
