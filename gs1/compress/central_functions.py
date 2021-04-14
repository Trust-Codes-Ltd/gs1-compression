from urllib.parse import unquote

from gs1.decompress.analyse_uri import extract_from_gs1_digital_link
from gs1.compress.build_compressed_gs1_digital_link import (
    build_compressed_gs1_digital_link)
from constants.regular_expressions import REGEX_ALL_NUM
from constants.ai_table import SHORT_CODE_TO_NUMERIC


def compress_gs1_digital_link(
        digital_link_uri,
        use_short_text,
        uri_stem,
        uncompressed_primary,
        use_optimizations,
        compress_other_key_value_pairs
):
    """Compress a full GS1 digital link."""
    query_string = ''
    non_gs1_key_value_pairs = {}
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
        gs1_array, use_short_text, uri_stem, use_optimizations,
        compress_other_key_value_pairs, non_gs1_key_value_pairs
    )
    return compressed_digital_link
