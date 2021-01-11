from gs1.utils import binary_to_hex
from constants.table_p import TABLE_P
from constants.table_opt import TABLE_OPT
from constants.alphabet import SAFE_BASE64_ALPHABET
from gs1.decompress.decode_binary_value import decode_binary_value, handle_decodings


def decompress_binary_to_gs1_array(binary_string):
    """Decompress a binary string and return an array """
    length = len(binary_string)
    cursor = 0
    gs1_ai_array = {}
    while length - cursor > 8:
        h1 = binary_to_hex("{0:0>X}", binary_string[cursor: cursor + 4])
        h2 = binary_to_hex("{0:0>X}", binary_string[cursor + 4: cursor + 8])
        h3 = ""
        app_identifier = ""
        h1_h2 = ''.join([h1, h2])
        cursor += 8
        d1 = int(h1, 16)
        d2 = int(h2, 16)
        if 0 <= d1 <= 9 and 0 <= d2 <= 9:
            # this means h1_h2 is between 00-99
            if h1_h2 in TABLE_P.keys():
                num_digits = TABLE_P.get(h1_h2)
                if num_digits == 2:
                    app_identifier = h1_h2
                elif num_digits in [3, 4]:
                    h3 = binary_to_hex(
                        "{0:0>X}", binary_string[cursor: cursor + 4])
                    cursor += 4
                    d3 = int(h3, 16)
                    if d3 > 9:
                        raise Exception(
                            "GS1 Application Identifier keys should be "
                            "all-numeric; " + h1_h2 + h3 + " is not all-numeric"
                        )
                    app_identifier = ''.join([h1_h2, h3])
                if num_digits == 4:
                    h4 = binary_to_hex(
                        "{0:0>X}", binary_string[cursor: cursor + 4])
                    cursor += 4
                    app_identifier = ''.join([h1_h2, h3, h4])
                    d4 = int(h4, 16)
                    if d4 > 9:
                        raise Exception(
                            "GS1 Application Identifier keys should be "
                            "all-numeric; " + h1_h2 + h3 + h4 +
                            " is not all-numeric"
                        )
                decoded_dict = decode_binary_value(
                    app_identifier, gs1_ai_array, binary_string, cursor)
                gs1_ai_array = decoded_dict.get('gs1AIarray')
                cursor = decoded_dict.get('cursor')
            else:
                raise Exception("Failure: Unsupported AI (reserved range) -"
                                f" no entry in tableP; h1h2={h1_h2}")
        else:
            # This case h1_h2 is outside 00-99. Hex characters will be used.
            if h1_h2 in TABLE_OPT.keys():
                sequence = TABLE_OPT.get(h1_h2)
                for bit in sequence:
                    tmp = decode_binary_value(
                        bit, gs1_ai_array, binary_string, cursor)
                    gs1_ai_array = tmp.get('gs1AIarray')
                    cursor = tmp.get('cursor')
            else:
                if h1 == 'F':
                    # handle decompression of non-GS1 key=value pairs
                    bits_including_f = binary_string[cursor - 8: cursor + 3]
                    key_length = int(binary_string[cursor - 4: cursor + 3], 2)
                    cursor += 3
                    key_bits = binary_string[cursor:cursor + 6 * key_length]
                    cursor += 6 * key_length
                    indices = [int(key_bits[6 * i: 6 * i + 6], 2)
                               for i in range(key_length)]
                    key = ''.join(
                        [SAFE_BASE64_ALPHABET[index] for index in indices])
                    encode_bits = binary_string[cursor: cursor + 3]
                    cursor += 3
                    encoded = int(encode_bits, 2)
                    num_char = int(binary_string[cursor: cursor + 7], 2)
                    cursor += 7
                    result = handle_decodings(
                        encoded, binary_string, cursor,
                        gs1_ai_array, key, num_char)
                    gs1_ai_array = result.get('gs1AIarray')
                    cursor = result.get('cursor')
                else:
                    raise Exception(
                        f"No optimisation defined for hex code hh={h1_h2}")
    return gs1_ai_array
