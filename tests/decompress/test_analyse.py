from unittest import TestCase

from gs1.constants import SAFE_BASE64_ALPHABET
from gs1.decompress.decode_binary_value import build_string, handle_decodings
from gs1.decompress.analyse_uri import analyse_uri, extract_from_compressed_gs1_digital_link


class TestBinaryDecode(TestCase):
    """Test cases for decompression functions."""

    def test_build_string(self):
        """Test build a base-64 string from a binary string."""
        binary_str = "10111110101111000010000000100101010101010101101111111101"
        result = build_string(3, SAFE_BASE64_ALPHABET, 0, 6, binary_str)
        self.assertEqual(result.get('s'), 'vrw')
        self.assertEqual(result.get('cursor'), 18)

    def test_handle_decodings(self):
        """Test handle decoding function."""
        binary_str = "10111110101111000010000000100101010101010101101111111101"
        handle_result = handle_decodings(0, binary_str, 0, {}, 'key', 3)
        self.assertEqual(handle_result.get('cursor'), 10)
        self.assertEqual(handle_result.get('gs1AIarray').get('key'), '762')


class TestAnalyseURI(TestCase):
    """Test case for the analyse URI function."""
    def test_analyse_uri(self):
        """Test the function analyse_uri."""
        analysed_result = analyse_uri('https://id.gs1.org/ARHKVAdpQg', False)
        self.assertEqual(analysed_result.get('compressedPath'), 'ARHKVAdpQg')
        self.assertEqual(analysed_result.get('uriPathInfo'), '/ARHKVAdpQg')
        extended_result = analyse_uri('https://id.gs1.org/ARHKVAdpQg', True)
        self.assertEqual(extended_result.get('elementStringsOutput'),
                         "(01)09780345418913")

    def test_extract(self):
        result = extract_from_compressed_gs1_digital_link(
            'https://id.gs1.org/ARHKVAdpQg')
        self.assertEqual(result.get('GS1').get('01'), '09780345418913')
