from math import ceil, log

from constants.alphabet import SAFE_BASE64_ALPHABET
from constants.regular_expressions import REGEX_ALL_NUM, CHAR_TO_ESCAPE
from constants.ai_table import AI_REGEX, AI_CHECK_DIGIT_POSITION


def number_of_length_bits(length: int):
    """

    :param length: Maximum permitted length.
    :return: The length indicator.
    """
    return ceil(log(length)/log(2) + 0.01)


def number_of_value_bits(value_bits: int):
    """
    The number of bits N required for an all-numeric fixed-length string.
    The binary value is left-padded (highest significant bits set to 0)
    in order to reach the total number of bits needed.

    :param value_bits: The fixed length number. For example, it's 14 for GTIN.
    :return: The length of bits to encode the string.
    """
    return ceil(value_bits * log(10)/log(2) + 0.01)


def base64_to_str(base64str):
    """Convert a base64 string to a binary string."""
    decimals = [SAFE_BASE64_ALPHABET.index(char) for char in base64str]
    binaries = ["{0:b}".format(decimal) for decimal in decimals]
    binaries = [binary if len(binary) >= 6 else binary.zfill(6)
                for binary in binaries]
    return ''.join(binaries)


def binary_to_hex(hex_format, binary_string) -> str:
    """
    Convert a binary string to a hexadecimal string.

    :param hex_format: hexadecimal format - "{0:0>X}" or "{0:0>2X}" etc.
    :param binary_string: binary string - for example, '1110'.
    :return: hexadecimal string - for example '0E', 'F'.
    """
    return hex_format.format(int(binary_string, 2))


def verify_syntax(app_identifier, value):
    """
    tests the syntax of a value against the regular expression (expected format)
    throws an error when invalid syntax is detected
    e.g. verifySyntax('01','01234567890128')
    """
    if app_identifier and REGEX_ALL_NUM.match(app_identifier):
        if not AI_REGEX[app_identifier].match(value):
            raise Exception("SYNTAX ERROR: invalid syntax for value"
                            " of (" + app_identifier + ")" + value)


def calculate_check_digit(app_identifier, gs1_id_value):
    """
    Calculate the expected GS1 Check Digit for a given AI
    e.g. calculateCheckDigit('01','01234567890128')
    """
    counter = 0
    total = 0
    if AI_CHECK_DIGIT_POSITION.get(app_identifier) == 'L':
        length_ = len(gs1_id_value)
    else:
        length_ = int(AI_CHECK_DIGIT_POSITION.get(app_identifier))
    for i in reversed(range(0, length_ - 1)):
        d = gs1_id_value[i:i + 2]
        if counter % 2 == 0:
            multiplier = 3
        else:
            multiplier = 1
        total += d * multiplier
        counter += 1
    return (10 - total % 10) % 10


def verify_check_digit(app_identifier, gs1_id_value):
    """returns true if the GS1 Check Digit is valid (or not applicable)
    throws an error if an invalid check digit is present
    e.g. verifyCheckDigit('01','01234567890128')
    """
    result = True
    check_digit_position = AI_CHECK_DIGIT_POSITION.get(app_identifier)
    if check_digit_position:
        expected_check_digit = calculate_check_digit(
            app_identifier, gs1_id_value)
        if check_digit_position == 'L':
            check_digit_position = len(gs1_id_value)
        else:
            check_digit_position = int(check_digit_position)
        actual_check_digit = int(gs1_id_value[check_digit_position - 1])
        if actual_check_digit != expected_check_digit:
            raise Exception("INVALID CHECK DIGIT:  An invalid check digit was"
                            " found for the primary identification key (" +
                            app_identifier + ")" + gs1_id_value +
                            " ; the correct check digit should be " +
                            str(expected_check_digit) + " at position " +
                            str(check_digit_position))
    return result


def pad_gtin(app_identifier, value):
    new_value = value
    # always pad the value of any GTIN [ AI (01) or (02) ] to 14 digits
    # in element string representation
    if app_identifier in ["01", "(01)", "02", "(02)"]:
        if len(value) == 8:
            new_value = ''.join(['000000', value])
        elif len(value) == 12:
            new_value = ''.join(['00', value])
        elif len(value) == 13:
            new_value = ''.join(['0', value])
    return new_value


def element_strings_push(element_strings, app_identifier, value, gs):
    new_value = pad_gtin(app_identifier, value)
    element_strings.append(''.join([app_identifier, new_value, gs]))
    return element_strings


def percent_encode(input_string: str):
    """
    Percent-code all reserved characters mentioned in the GS1 Digital Link
    standard.
    """
    length_ = len(input_string)
    escaped_chars = [''.join(['%', format(ord(char[0]), 'x').upper()])
                     if input_string.index(char) < length_ - 1 else char
                     for char in input_string]
    return ''.join(escaped_chars)
