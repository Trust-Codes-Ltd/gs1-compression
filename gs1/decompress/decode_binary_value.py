from gs1.constants import TABLE_F
from gs1.constants import HEX_ALPHABET, SAFE_BASE64_ALPHABET
from gs1.utils import number_of_value_bits, number_of_length_bits


def build_string(num_char, alphabet, cursor, multiplier, binary_string):
    result = {}
    num_bits_for_value = multiplier * num_char
    sub_str = binary_string[cursor:cursor + num_bits_for_value]
    cursor += num_bits_for_value
    indices = [int(sub_str[multiplier * i:multiplier * (i + 1)], 2)
               for i in range(num_char)]
    string_ = ''.join([chr(int(index)) if multiplier == 7
                      else alphabet[index] for index in indices])
    result['cursor'] = cursor
    result['s'] = string_
    return result


def handle_decodings(enc, binary_string, cursor, gs1_ai_array, key, num_char):
    """
    Handle decodings.

    this method determines how many bits to extract (depending on the encoding),
    extracts those bits, advances the cursor and converts the extracted bits
    into a string value in the appropriate encoding, which is then inserted into
    the specified associative array, the updated associative array and
    updated binary string cursor position are returned.

    :param enc: a specified encoding enc (in range 0-4).
    :param binary_string: binary string.
    :param cursor: binary string cursor position.
    :param gs1_ai_array: GS1 application identifier dict.
    :param key: Key.
    :param num_char: number of characters to extract.
    :return:
    """
    result = {}
    if key not in gs1_ai_array:
        gs1_ai_array[key] = ''
    if enc == 0:
        num_bits_for_value = number_of_value_bits(num_char)
        sub_str = binary_string[cursor:cursor + num_bits_for_value]
        cursor += num_bits_for_value
        gs1_ai_array[key] += str(int(sub_str, 2))
    elif enc == 1:
        result = build_string(num_char, HEX_ALPHABET, cursor, 4, binary_string)
        cursor = result.get('cursor')
        gs1_ai_array[key] += result.get('s').lower()
    elif enc == 2:
        result = build_string(num_char, HEX_ALPHABET, cursor, 4, binary_string)
        cursor = result.get('cursor')
        gs1_ai_array[key] += result.get('s').upper()
    elif enc == 3:
        result = build_string(
            num_char, SAFE_BASE64_ALPHABET, cursor, 6, binary_string)
        cursor = result.get('cursor')
        gs1_ai_array[key] += result.get('s')
    elif enc == 4:
        result = build_string(num_char, '', cursor, 7, binary_string)
        cursor = result.get('cursor')
        gs1_ai_array[key] += result.get('s')
    result['gs1AIarray'] = gs1_ai_array
    result['cursor'] = cursor
    return result


def decode_binary_value(key, gs1_array, binary_string, cursor):
    result = {}
    gs1_array[key] = ""
    if key in TABLE_F.keys():
        for type_dict in TABLE_F.get(key):
            if 'L' in type_dict.keys() and type_dict.get('E', '') == 'N':
                # This indicates it's fixed length, so no length indicator
                bits = number_of_value_bits(int(type_dict.get('L')))
                sub_str = binary_string[cursor:bits + cursor]
                cursor += bits
                s = str(int(sub_str, 2)).zfill(int(type_dict.get('L')))
                gs1_array[key] += s
            if 'M' in type_dict.keys() and type_dict.get('E', '') == 'N':
                # handle variable-length numeric component
                values = number_of_length_bits(int(type_dict.get('M')))
                length_bits = binary_string[cursor:values + cursor]
                cursor += values
                num_digits = int(length_bits, 2)
                num_bits_for_value = number_of_value_bits(num_digits)
                sub_str = binary_string[cursor:num_bits_for_value + cursor]
                cursor += num_bits_for_value
                if num_digits:
                    s = "{0:b}".format(int(sub_str, 2))
                else:
                    s = ""
                gs1_array[key] += s
            if 'L' in type_dict.keys() and type_dict.get('E', '') == 'X':
                # handle fixed-length alphanumeric component
                encoded_bits = binary_string[cursor:cursor + 3]
                cursor += 3
                encoded_int = int(encoded_bits, 2)
                num_char = type_dict.get('L')
                sub_str = handle_decodings(encoded_int, binary_string, cursor,
                                           gs1_array, key, num_char)
                gs1_array = sub_str.get('gs1AIarray')
                cursor = sub_str.get('cursor')
            if 'M' in type_dict.keys() and type_dict.get('E', '') == 'X':
                # Handle variable-length alphanumeric component
                encoded_bits = binary_string[cursor:cursor + 3]
                cursor += 3
                values = number_of_length_bits(int(type_dict.get('M')))
                length_bits = binary_string[cursor:cursor + values]
                cursor += values
                num_char = int(length_bits, 2)
                encoded_int = int(encoded_bits, 2)
                sub_str = handle_decodings(encoded_int, binary_string, cursor,
                                           gs1_array, key, num_char)
                gs1_array = sub_str.get('gs1AIarray')
                cursor = sub_str.get('cursor')
    result['gs1AIarray'] = gs1_array
    result['cursor'] = cursor
    return result
