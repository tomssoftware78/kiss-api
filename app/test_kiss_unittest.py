import unittest

from app.main import convertKissDetailToItemID, convertKissDetailToCaseID, convertCaseIDToKissDetail, \
    convertItemIDToKissDetail, convertKissDetailToCaseName


class MyTestCase(unittest.TestCase):

    def test_conversion(self):
        self.assertEqual(220055003, convertKissDetailToItemID("RCCU/22/0055/003"))
        self.assertEqual("22/0055", convertKissDetailToCaseName("RCCU/22/0055/003"))
        self.assertEqual(220055, convertKissDetailToCaseID("RCCU/22/0055/003"))
        self.assertEqual("RCCU/22/0055/", convertCaseIDToKissDetail(220055))
        self.assertEqual("RCCU/22/0055/003", convertItemIDToKissDetail(220055003))

if __name__ == '__main__':
    unittest.main()
