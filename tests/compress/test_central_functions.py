from unittest import TestCase

from gs1.compress.core_functions import *


class TestCentralFunctions(TestCase):
    """Test the core functions to compress a digital link."""
    def setUp(self):
        """Test class setup."""
        self.long_digital_link = ('https://truea2.com/gtin/9421902960055/'
                                  'lot/2010005828/ser/xyz1234')
        self.expansive_link = (
            "https://truea2.com/01/05412345000013/10/"
            "ABC%26%2B123?7003=1903061658&k1=v1"
        )

    def test_compress_gs1_digital_link(self):
        """Test compressing a digital link."""
        result = compress_gs1_digital_link(
            self.long_digital_link, 'https://truea2.com')
        self.assertEqual(
            result, "https://truea2.com/AREjalurbiAUO-cgohCz45Z67b8A")
        result_long = compress_gs1_digital_link(
            self.expansive_link, 'https://truea2.com', None, True
        )
        self.assertEqual(result_long.split('/')[-1],
                         'AQnYUc1gmiERBhQ0ytiyZuAGOLc1TXgpNWCv1')
