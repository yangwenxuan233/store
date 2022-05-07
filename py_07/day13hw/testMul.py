import unittest
from Calc import Calc


class TestCalc_mul(unittest.TestCase):

    def testmul1(self):
        a = 2
        b = 3
        c = 6
        calc = Calc()
        pro = calc.mul(a, b)
        self.assertEqual(c, pro)

    def testmul2(self):
        a = 2
        b = 3
        c = 4
        calc = Calc()
        pro = calc.mul(a, b)
        self.assertEqual(c, pro)

    def testmul3(self):
        a = 2
        b = 3
        c = 6
        calc = Calc()
        pro = calc.mul(a, b)
        self.assertEqual(c, pro)

    def testmul4(self):
        a = -2
        b = 3
        c = -6
        calc = Calc()
        pro = calc.mul(a, b)
        self.assertEqual(c, pro)

    def testmul5(self):
        a = 2
        b = -3
        c = 6
        calc = Calc()
        pro = calc.mul(a, b)
        self.assertEqual(c, pro)

    def testmul6(self):
        a = -2
        b = -3
        c = 6
        calc = Calc()
        pro = calc.mul(a, b)
        self.assertEqual(c, pro)
