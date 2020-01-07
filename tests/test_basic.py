from twisted.trial import unittest

class BasicTest(unittest.TestCase):

    def setUp(self):
        self.basic = "basic"


    def testBasic1(self):

        self.assertTrue(1 == 1)
