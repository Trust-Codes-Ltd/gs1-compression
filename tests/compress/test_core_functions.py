from unittest import TestCase

from gs1.compress.core_functions import *


class TestCentralFunctions(TestCase):
    """Test the core functions to compress a digital link."""
    def setUp(self):
        """Test class setup."""
        self.long_digital_link = ('https://id.gs1.org/gtin/9421902960055/'
                                  'lot/2010005828/ser/xyz1234')
        self.link_sscc = 'https://id.gs1.org/00/106141412345678908'
        self.link_gln = 'https://id.gs1.org/414/0614141123452'
        self.expansive_link = (
            "https://id.gs1.org/01/05412345000013/10/"
            "ABC%26%2B123?7003=1903061658&k1=v1"
        )
        self.link_8003 = ("https://example.com/8003/09421012301014f9804dbf"
                          "?240=qwe390023")
        self.element_string = "(01)00614141123452(3103)000500"
        self.element_string_no_bracket = (
                "3103000189010541234500001339232172" + '\x1d' + '10ABC123')

    def test_compress_gs1_digital_link(self):
        """Test compressing a digital link."""
        result = compress_gs1_digital_link(self.long_digital_link)
        self.assertEqual(
            result, "https://id.gs1.org/AREjalurbiAUO-cgohCz45Z67b8A")
        result_long = compress_gs1_digital_link(
            self.expansive_link, False, True)
        self.assertEqual(result_long.split('/')[-1],
                         'AQnYUc1gmiERBhQ0ytiyZuAGOLc1TXgpNWCv1')
        result_sscc = compress_gs1_digital_link(self.link_sscc)
        self.assertEqual(result_sscc.split('/')[-1], 'ABeRcNWtKMPA')
        result_gln = compress_gs1_digital_link(self.link_gln)
        self.assertEqual(result_gln.split('/')[-1], 'QUCO_anbfA')
        result_8003 = compress_gs1_digital_link(self.link_8003)
        self.assertEqual(result_8003.split('/')[-1],
                         'JAaasHt_dNNt4ADESMALumsUfMAm34')

    def test_element_string_to_compressed_gs1_digital_link(self):
        """Test compressing a digital link element string."""
        result = element_string_to_compressed_gs1_digital_link(
            self.element_string, False, 'https://id.gs1.org', False, False
        )
        self.assertEqual(result, 'https://id.gs1.org/AQEd-1O2-GIGAD6A')

        result_no_bracket = element_string_to_compressed_gs1_digital_link(
            self.element_string_no_bracket, False, 'https://id.gs1.org',
            False, False)
        self.assertEqual(result_no_bracket,
                         'https://id.gs1.org/AQnYUc1gmiCNV4JGYgYAF6ckaEPg')
