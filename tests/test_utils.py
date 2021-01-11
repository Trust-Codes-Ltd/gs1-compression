from unittest import TestCase

from gs1.utils import (
    number_of_value_bits, number_of_length_bits,
    base64_to_str, binary_to_hex, percent_encode,
    pad_gtin, element_strings_push, calculate_check_digit,
    verify_check_digit,
)


class TestNumericalFunctions(TestCase):
    """Test case for the two basic numerical functions."""
    def test_number_of_length_bits(self):
        """Test number_of_length_bits."""
        self.assertEqual(number_of_length_bits(10), 4)

    def test_number_of_value_bits(self):
        """Test number_of_value_bits."""
        self.assertEqual(number_of_value_bits(10), 34)


class TestStringTransformation(TestCase):
    """Test case for base64_to_str and binary_to_hex."""
    def test_base64_to_str(self):
        """Test transformation from base64 string to binary string."""
        self.assertEqual(base64_to_str('cbd'), '011100011011011101')

    def test_binary_to_hex(self):
        """Test transformation from binary string to hex string."""
        self.assertEqual(binary_to_hex("{0:0>X}", '1010'), 'A')


class TestPercentEncode(TestCase):
    """Test case for percent encode function."""
    def test_percent_encode(self):
        """Test encoding a special character."""
        self.assertEqual(percent_encode('&'), '%26')


class TestPadGTIN(TestCase):
    """Test case for pad gtin function."""
    def test_pad_gtin(self):
        """Test left-padding gtin with zeros."""
        value_8 = '12345678'
        value_12 = '123456789011'
        value_13 = '1234567890114'
        self.assertEqual(pad_gtin('01', value_8), '000000' + value_8)
        self.assertEqual(pad_gtin('02', value_12), '00' + value_12)
        self.assertEqual(pad_gtin('(01)', value_13), '0' + value_13)
        self.assertEqual(pad_gtin('ddd', value_13), value_13)

    def test_element_strings_push(self):
        """Test the function of pushing element strings."""
        self.assertEqual(
            element_strings_push(['ss'], '01', '12345678', ''),
            ['ss', '0100000012345678']
        )


class TestCalculations(TestCase):
    """Testcase for calculate_check_digit."""
    def test_calculate_check_digit(self):
        """Test calculate_check_digit function."""
        self.assertEqual(calculate_check_digit('01', '01234567890128'), 8)

    def test_verify_check_digit(self):
        """Test verify_check_digit function."""
        self.assertEqual(verify_check_digit('01', '01234567890128'), True)
