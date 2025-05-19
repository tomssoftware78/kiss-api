import unittest

from service.kiss_tools import KissTools

class MyTestCase(unittest.TestCase):

    def test_conversion(self):
        self.assertEqual(220055003, KissTools.convertKissDetailToItemID("RCCU/22/0055/003"))
        self.assertEqual("22/0055", KissTools.convertKissDetailToCaseName("RCCU/22/0055/003"))
        self.assertEqual(220055, KissTools.convertKissDetailToCaseID("RCCU/22/0055/003"))
        self.assertEqual("RCCU/22/0055/", KissTools.convertCaseIDToKissDetail(220055))
        self.assertEqual("RCCU/22/0055/003", KissTools.convertItemIDToKissDetail(220055003))

if __name__ == '__main__':
    unittest.main()
