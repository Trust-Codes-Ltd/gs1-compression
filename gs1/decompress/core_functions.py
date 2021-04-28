from gs1.utils import parse_url
from gs1.decompress.analyse_uri import extract_from_compressed_gs1_digital_link
from gs1.decompress.build_gs1_digital_link import build_gs1_digital_link
from gs1.decompress.build_structured_array import build_structured_array
from gs1.decompress.deal_with_duplicates import deal_with_duplicates


def decompress_gs1_digital_link(
        compressed_digital_link_uri: str, use_short_text: bool):
    """
    Decompress a compressed GS1 digital link URI.

    For example, https://id.gs1.org/ARHKVAdpQg corresponds to
    https://id.gs1.org/01/09780345418913. If a short text is preferred, the
    result will be https://id.gs1.org/gtin/09780345418913 instead.

    :param compressed_digital_link_uri: Compressed digital link URI.
    :param use_short_text: Bool, indicating if a short text is preferred.
    :return: uncompressed GS1 digital link.
    """
    parsed_url = parse_url(url=compressed_digital_link_uri)
    uri_stem = parsed_url[0]
    extracted = extract_from_compressed_gs1_digital_link(
        compressed_digital_link_uri)
    gs1_ai_array = extracted.get('GS1')
    gs1_ai_array = deal_with_duplicates(gs1_ai_array)
    other_array = extracted.get('other')
    return build_gs1_digital_link(
        gs1_ai_array, use_short_text, uri_stem, other_array)


def decompress_gs1_digital_link_to_structured_array(
        compressed_digital_link_uri: str) -> dict:
    """
    Analyze a compressed GS1 digital link URI and extract information about
    identifiers, qualifiers, data attributes and others.

    For example, the structured array for https://id.gs1.org/ARHKVAdpQg is:
    {
        "identifiers": [{"01": "09780345418913"}],
        "qualifiers": [],
        "dataAttributes": [],
        "other": []
    }

    :param compressed_digital_link_uri: compressed digital link URI.
    :return: Dict of identifier, qualifier, data attributes and other info.
    """
    extracted = extract_from_compressed_gs1_digital_link(
        compressed_digital_link_uri)
    gs1_ai_array = extracted.get('GS1')
    gs1_ai_array = deal_with_duplicates(gs1_ai_array)
    other_array = extracted.get('other')
    return build_structured_array(gs1_ai_array, other_array)
