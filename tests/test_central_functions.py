from unittest import TestCase

from gs1.decompress.central_functions import decompress_gs1_digital_link


class TestDecompressGS1DigitalLink(TestCase):
    """Test case for the central function of decompressing digital link."""
    def test_decompress_gs1_digital_link(self):
        """Test decompress_gs1_digital_link."""
        self.assertEqual(
            decompress_gs1_digital_link(
                "https://dlnkd.tn.gg/ARHKVAdpQg", False, "https://dlnkd.tn.gg"),
            'https://dlnkd.tn.gg/01/09780345418913'
        )
        self.assertEqual(
            decompress_gs1_digital_link(
                "http://example.org/AQnYUc1gmiER"
                "BhQ0ytiyZuAGOLc1TXhXsaXbQKHFuaprwUmrBX6g",
                False, "http://example.org"
            ),
            "http://example.org/01/05412345000013/10/ABC%26%2B123?7003="
            "1903061658&expdt=1903061658&k1=v1"
        )
