from urllib.parse import unquote

from gs1.decompress.analyse_uri import extract_from_gs1_digital_link
from gs1.decompress.core_functions import build_gs1_digital_link
from gs1.compress.build_compressed_gs1_digital_link import (
    build_compressed_gs1_digital_link, compress_gs1_ai_array_to_binary)
from gs1.compress.utils import separate_id_non_id
from gs1.compress.extract_from_element_strings import (
    extract_from_element_strings)
from gs1.utils import binary_to_base64, parse_url
from gs1.constants import REGEX_ALL_NUM
from gs1.constants import SHORT_CODE_TO_NUMERIC


def compress_gs1_digital_link(
        digital_link_uri: str,
        use_optimizations: bool = False,
        compress_other_key_value_pairs: bool = False
) -> str:
    """Compress a full GS1 digital link."""
    query_string = ''
    non_gs1_key_value_pairs = {}
    parse_result = parse_url(digital_link_uri)
    uri_stem = parse_result[0]
    if "?" in digital_link_uri:
        first_question_mark = digital_link_uri.index("?")
        query_string = digital_link_uri[1 + first_question_mark:]
    if query_string:
        query_string = query_string.replace(';', '&')
        if '#' in query_string:
            first_fragment = query_string.index('#')
            query_string = query_string[:first_fragment]
        pairs = query_string.split('&')
        pair_list = [p.split('=') for p in pairs]
        non_gs1_key_value_pairs = {
            p[0]: unquote(p[1]) for p in pair_list
            if (p[0] and p[1] and not REGEX_ALL_NUM.match(p[0]) and
                p[0] not in SHORT_CODE_TO_NUMERIC.keys())
        }
    gs1_array = extract_from_gs1_digital_link(digital_link_uri).get('GS1')
    compressed_digital_link = build_compressed_gs1_digital_link(
        gs1_array, uri_stem, use_optimizations,
        compress_other_key_value_pairs, non_gs1_key_value_pairs
    )
    return compressed_digital_link


def element_string_to_compressed_gs1_digital_link(
        element_string,
        use_short_text,
        uri_stem,
        uncompressed_primary=None,
        use_optimization=False
):
    """Build a compressed GS1 digital link from an element string."""
    gs1_ai_array = extract_from_element_strings(element_string)
    separated_result = separate_id_non_id(gs1_ai_array)
    if uncompressed_primary:
        compressed_non_id_part = compress_gs1_ai_array_to_binary(
            separated_result['nonID'], use_optimization, {}
        )
        compressed_id_part = build_gs1_digital_link(
            separated_result.get('ID'), use_short_text, uri_stem, {}
        )
        return (compressed_id_part + '/' +
                binary_to_base64(compressed_non_id_part))
    else:
        return build_compressed_gs1_digital_link(
            gs1_ai_array, uri_stem, use_optimization, False, {}
        )
