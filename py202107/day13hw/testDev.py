import unittest
from Calc import Calc


class TestCalc_dec(unittest.TestCase):

    def testdec1(self):
        a = 4
        b = 2
        c = 2
        calc = Calc()
        que = calc.dev(a, b)
        self.assertEqual(c, que)

    def testdec2(self):
        a = 4
        b = 2
        c = 3
        calc = Calc()
        que = calc.dev(a, b)
        self.assertEqual(c, que)

    def testdec3(self):
        a = -4
        b = 2
        c = -2
        calc = Calc()
        que = calc.dev(a, b)
        self.assertEqual(c, que)

    def testdec4(self):
        a = 4
        b = -2
        c = 2
        calc = Calc()
        que = calc.dev(a, b)
        self.assertEqual(c, que)

    def testdec5(self):
        a = -4
        b = -2
        c = 2
        calc = Calc()
        que = calc.dev(a, b)
        self.assertEqual(c, que)

    def testdec6(self):
        a = -4
        b = -2
        c = -2
        calc = Calc()
        que = calc.dev(a, b)
        self.assertEqual(c, que)
