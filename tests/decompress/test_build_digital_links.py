from unittest import TestCase

from gs1.decompress.build_gs1_digital_link import build_gs1_digital_link


class TestBuildDigitalLink(TestCase):
    """Test case for building GS1 digital link."""
    def test_build_gs1_digital_link(self):
        """Test build_gs1_digital_link."""
        uri_stem = "https://id.gs1.org"
        array = {"10": "2010005828", "21": "xyz1234", "01": "09421902960055"}
        self.assertEqual(
            build_gs1_digital_link(array, False, uri_stem, {}),
            'https://id.gs1.org/01/09421902960055/10/2010005828/21/xyz1234'
        )
