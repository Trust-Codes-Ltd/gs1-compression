from unittest import TestCase

from gs1.decompress.core_functions import decompress_gs1_digital_link


class TestDecompressGS1DigitalLink(TestCase):
    """Test case for the central function of decompressing digital link."""
    def test_decompress_gs1_digital_link(self):
        """Test decompress_gs1_digital_link."""
        self.assertEqual(
            decompress_gs1_digital_link(
                "https://id.gs1.org/ARHKVAdpQg", False),
            'https://id.gs1.org/01/09780345418913'
        )
        self.assertEqual(
            decompress_gs1_digital_link(
                "http://example.org/AQnYUc1gmiERBhQ0ytiyZuAGOLc1TXgpNWCv1",
                False
            ),
            "http://example.org/01/05412345000013/10/ABC%26%2B123?7003="
            "1903061658&k1=v1"
        )

    def test_decompress_without_gtin(self):
        """Test decompression of GS1 digital links without GTIN."""
        self.assertEqual(
            decompress_gs1_digital_link(
                "https://id.gs1.org/ABeRcNWtKMPA", True),
            'https://id.gs1.org/sscc/106141412345678908'
        )
        self.assertEqual(
            decompress_gs1_digital_link(
                "https://id.gs1.org/QUCO_anbfA", False),
            'https://id.gs1.org/414/0614141123452'
        )
        self.assertEqual(
            decompress_gs1_digital_link(
                "https://id.gs1.org/JAaasHt_dNNt4ADESMALumsUfMAm34", False),
            "https://id.gs1.org/8003/09421012301014f9804dbf?240=qwe390023"
        )
