from gs1.utils import number_of_value_bits, number_of_length_bits

from gs1.constants import TABLE_F
from gs1.constants import (
    REGEX_ALL_NUM, REGEX_SAFE_64, REGEX_HEX_LOWER, REGEX_HEX_UPPER)
from gs1.constants import HEX_ALPHABET, SAFE_BASE64_ALPHABET


def determine_encoding(char_string) -> int:
    """
    Determine the way to encode a string based on regex.

    :param char_string: String.
    :return: the type of encoding.
    """
    if REGEX_ALL_NUM.match(char_string):
        return 0
    elif REGEX_HEX_UPPER.match(char_string):
        return 2
    elif REGEX_HEX_LOWER.match(char_string):
        return 1
    elif REGEX_SAFE_64.match(char_string):
        return 3
    else:
        return 4


def build_binary_value(char_str, bits, alphabet) -> str:
    """
    This method converts a string char_str into binary, using n bits per
    character and decoding from the supplied alphabet or from ASCII when bits=7

    This is almost the inverse method to build_string in the decompress module.

    :param char_str: string.
    :param bits: number of bits per character.
    :param alphabet: Alphabet.
    :return: binary value.
    """
    if bits == 7:
        indices = [ord(char_) for char_ in char_str]
    else:
        indices = [alphabet.index(char_) for char_ in char_str]
    binary_char_list = ["{0:b}".format(index).zfill(bits) for index in indices]
    return ''.join(binary_char_list)


def handle_encoding(enc, length_bits, char_str: str, binary_string):
    """
    Creates a binary string fragment that starts with a 3-digit encoding
    indicator, any lengthBits specified (empty string "" if not required for a
    fixed-length value) and then the actual value of char_str in
    binaryEncodingOfGS1AIKey.

    Calls buildBinaryValue() when encoding the value in binary.

    :param enc: Encoding type.
    :param length_bits: Length bits.
    :param char_str:
    :param binary_string:
    :return: Binary string fragment.
    """
    if enc == 0:
        binary_length = number_of_value_bits(len(char_str))
        binary_value = "{0:b}".format(int(char_str)).zfill(binary_length)
        binary_string += '000' + length_bits + binary_value
    elif enc == 1:
        binary_string += '001' + length_bits + build_binary_value(
            char_str.upper(), 4, HEX_ALPHABET)
    elif enc == 2:
        binary_string += '010' + length_bits + build_binary_value(
            char_str.upper(), 4, HEX_ALPHABET)
    elif enc == 3:
        binary_string += '011' + length_bits + build_binary_value(
            char_str, 6, SAFE_BASE64_ALPHABET)
    elif enc == 4:
        binary_string += '100' + length_bits + build_binary_value(
            char_str, 7, alphabet=None)
    return binary_string


def binary_encoding_gs1_ai_key(key: str):
    """
    Encode a GS1 application identifier key into a binary number.
    :param key: GS1 application identifier key.
    :return: Encoded binary string.
    """
    binary_ai_key = ''.join(["{0:b}".format(int(char_, 16)).zfill(4)
                             for char_ in key])
    return binary_ai_key


def binary_encoding_value(gs1_ai_array: dict, key: str):
    """
    Encode an application identifier value to binary string.
    :param gs1_ai_array: application identifier value.
    :param key: Key.
    :return: Encoded binary string.
    """
    binary_str = ''
    if key in TABLE_F.keys():
        cursor = 0
        value = gs1_ai_array.get(key)
        for ai_value in TABLE_F.get(key):
            if 'L' in ai_value.keys() and ai_value.get('E') == "N":
                # Handle fixed-length numeric component
                char_str = value[cursor:cursor + int(ai_value.get('L'))]
                cursor += int(ai_value.get('L'))
                binary_value = "{0:b}".format(int(char_str)).zfill(
                    number_of_value_bits(int(ai_value.get('L'))))
                binary_str += binary_value
            if 'M' in ai_value.keys() and ai_value.get('E') == "N":
                # Handle variable-length numeric component
                char_str = value[cursor:]
                cursor += len(char_str)
                length_bits = "{0:b}".format(len(char_str)).zfill(
                    number_of_length_bits(int(ai_value.get('M'))))
                binary_value = "{0:b}".format(int(char_str)).zfill(
                    number_of_value_bits(len(char_str)))
                binary_str += length_bits + binary_value
            if 'L' in ai_value.keys() and ai_value.get('E') == "X":
                # Handle fixed-length alphanumeric component
                char_str = value[cursor: cursor + int(ai_value.get('L'))]
                cursor += int(ai_value.get('L'))
                encoding_type = determine_encoding(char_str)
                length_bits = ''
                binary_str = handle_encoding(
                    encoding_type, length_bits, char_str, binary_str)
            if 'M' in ai_value.keys() and ai_value.get('E') == "X":
                # Handle variable-length alphanumeric component.
                char_str = value[cursor:]
                cursor += len(char_str)
                length_bits = "{0:b}".format(len(char_str)).zfill(
                    number_of_length_bits(int(ai_value.get('M'))))
                encoding_type = determine_encoding(char_str)
                binary_str = handle_encoding(
                    encoding_type, length_bits, char_str, binary_str)
    return binary_str


def binary_encoding_non_gs1_value(char_str):
    """
    Encode a non-GS1 value into binary string.

    :param char_str: Non-GS1 value.
    :return: encoded binary string.
    """
    length_bits = "{0:b}".format(len(char_str)).zfill(7)
    encoding_type = determine_encoding(char_str)
    binary_str = handle_encoding(encoding_type, length_bits, char_str, "")
    return binary_str
