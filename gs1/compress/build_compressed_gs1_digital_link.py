from gs1.compress.utils import (
    find_candidates_from_table_opt,
    find_best_optimization_candidate,
    remove_optimized_key_from_ai_list
)
from gs1.compress.encode_binary_value import (
    binary_encoding_value,
    binary_encoding_gs1_ai_key,
    binary_encoding_non_gs1_value
)
from gs1.utils import binary_to_base64

from gs1.constants import TABLE_OPT
from gs1.constants import SAFE_BASE64_ALPHABET


def compress_gs1_ai_array_to_binary(
        gs1_ai_array: dict,
        use_optimizations,
        non_gs1_key_value_pairs
):
    """
    Compress GS1 application identifier array to a binary string.

    :param gs1_ai_array: gs1 AI array.
    :param use_optimizations: Boolean, whether to use optimizations.
    :param non_gs1_key_value_pairs: non GS1 key value pairs.
    :return: binary string of compressed data.
    """
    binary_str = ''
    gs1_keys = sorted(gs1_ai_array.keys())
    optimizations = []
    if use_optimizations:
        candidates_from_table_opt = {'sample': 'sample'}
        while len(candidates_from_table_opt.keys()) > 0:
            candidates_from_table_opt = find_candidates_from_table_opt(gs1_keys)
            # pick candidatesFromTableOpt that can save
            # the highest number of AI key characters.
            best_candidate = find_best_optimization_candidate(
                candidates_from_table_opt)
            if best_candidate:
                gs1_keys = remove_optimized_key_from_ai_list(
                    gs1_keys, TABLE_OPT.get(best_candidate))
                optimizations.append(best_candidate)
            candidates_from_table_opt = find_candidates_from_table_opt(gs1_keys)

    # Encode binary string for any optimised values from tableOpt first.
    for optimization in optimizations:
        binary_str += binary_encoding_gs1_ai_key(optimization)
        opt_array = TABLE_OPT.get(optimization)
        binary_str += ''.join([binary_encoding_value(gs1_ai_array, value)
                               for value in opt_array.values()])
    # Then append this further, by encoding binary string values for any other
    # AI key-value pairs, for which no optimisations were found.
    bin_lists = [
        binary_encoding_gs1_ai_key(key) +
        binary_encoding_value(gs1_ai_array, key)
        for key in gs1_keys if key in gs1_ai_array.keys()
    ]
    binary_str += ''.join(bin_lists)
    # Then if any non-GS1 key=value pairs were also to be compressed, also
    # compress those and append to the binary string.

    # Note that hex value F ('1111') is used as a flag
    # (as a reserved value of h1) to indicate that what follows is a compressed
    # binary representation of a non-GS1 key-value pair.

    # We permit key lengths up to 128 characters only from the URI-safe base64
    # alphabet (A-Z a-z 0-9 hyphen and underscore).
    if len(non_gs1_key_value_pairs.keys()) > 0:
        for key, value in non_gs1_key_value_pairs.items():
            length_bits = "{0:b}".format(len(key)).zfill(7)
            binary_str += '1111'  # flag for non-GS1 keys that will follow
            binary_str += length_bits
            binary_key = ''.join(
                [
                    "{0:b}".format(SAFE_BASE64_ALPHABET.index(char_)).zfill(6)
                    for char_ in key
                ])
            binary_str += binary_key
            binary_str += binary_encoding_non_gs1_value(value)
    return binary_str


def build_compressed_gs1_digital_link(
        gs1_ai_array,
        uri_stem: str,
        use_optimizations,
        compress_other_keypairs,
        non_gs1_key_value_pairs
):
    """

    Build a compressed gs1 digital link with a GS1 application identifier array.

    :param gs1_ai_array: GS1 application identifier array.
    :param uri_stem: URI prefix. Default being https://id.gs1.org
    :param use_optimizations: Boolean.
    :param compress_other_keypairs: Boolean.
    :param non_gs1_key_value_pairs: Non GS1 key value pairs.
    :return: compressed gs1 digital link URI.
    """
    query_string = ''
    canonical_stem = 'https://id.gs1.org'
    if not compress_other_keypairs:
        # This means other key pairs won't be compressed.
        non_gs1_key_value_list = [
            f'{key}={value}' for key, value in non_gs1_key_value_pairs]
        if len(non_gs1_key_value_list) > 0:
            query_string = '?' + '&'.join(non_gs1_key_value_list)
    if uri_stem and uri_stem.endswith('/'):
        # Remove unwanted trailing slash
        uri_stem = uri_stem[:-1]
    if compress_other_keypairs:
        binary_str = compress_gs1_ai_array_to_binary(
            gs1_ai_array, use_optimizations, non_gs1_key_value_pairs)
    else:
        binary_str = compress_gs1_ai_array_to_binary(
            gs1_ai_array, use_optimizations, {})
    path = '/' + binary_to_base64(binary_str)
    if not uri_stem:
        web_uri = canonical_stem + path + query_string
    else:
        web_uri = uri_stem + path + query_string
    return web_uri
