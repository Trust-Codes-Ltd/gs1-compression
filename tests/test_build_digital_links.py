from unittest import TestCase

from gs1.decompress.build_gs1_digital_link import build_gs1_digital_link


class TestBuildDigitalLink(TestCase):
    """Test case for building GS1 digital link."""
    def test_build_gs1_digital_link(self):
        """Test build_gs1_digital_link."""
        self.assertEqual(
            build_gs1_digital_link(),
            ''
        )
