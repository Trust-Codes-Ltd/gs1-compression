from decompress.extract import extract_from_compressed_gs1_digital_link
from decompress.build_gs1_digital_link import build_gs1_digital_link
from decompress.build_structured_array import build_structured_array


def decompress_gs1_digital_link(
        compressed_digital_link_uri, use_short_text, uri_stem):
    extracted = extract_from_compressed_gs1_digital_link(
        compressed_digital_link_uri)
    gs1_ai_array = extracted.get('GS1')
    other_array = extracted.get('other')
    return build_gs1_digital_link(
        gs1_ai_array, use_short_text, uri_stem, other_array)


def decompress_gs1_digital_link_to_structured_array(
        compressed_digital_link_uri):
    extracted = extract_from_compressed_gs1_digital_link(
        compressed_digital_link_uri)
    gs1_ai_array = extracted.get('GS1')
    other_array = extracted.get('other')
    return build_structured_array(gs1_ai_array, other_array)
