from gs1.decompress.analyse_uri import extract_from_compressed_gs1_digital_link
from gs1.decompress.build_gs1_digital_link import build_gs1_digital_link
from gs1.decompress.build_structured_array import build_structured_array


def decompress_gs1_digital_link(
        compressed_digital_link_uri: str, use_short_text: bool, uri_stem):
    """
    Decompress a compressed GS1 digital link URI.

    For example, https://dlnkd.tn.gg/ARHKVAdpQg corresponds to
    https://dlnkd.tn.gg/01/09780345418913. If a short text is preferred, the
    result will be https://dlnkd.tn.gg/gtin/09780345418913 instead.

    :param compressed_digital_link_uri: Compressed digital link URI.
    :param use_short_text: Bool, indicating if a short text is preferred.
    :param uri_stem: URI prefix. If not specified, a canonical one will be used.
    :return: uncompressed GS1 digital link.
    """
    extracted = extract_from_compressed_gs1_digital_link(
        compressed_digital_link_uri)
    gs1_ai_array = extracted.get('GS1')
    other_array = extracted.get('other')
    return build_gs1_digital_link(
        gs1_ai_array, use_short_text, uri_stem, other_array)


def decompress_gs1_digital_link_to_structured_array(
        compressed_digital_link_uri: str) -> dict:
    """
    Analyze a compressed GS1 digital link URI and extract information about
    identifiers, qualifiers, data attributes and others.

    For example, the structured array for https://dlnkd.tn.gg/ARHKVAdpQg is:
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
    other_array = extracted.get('other')
    return build_structured_array(gs1_ai_array, other_array)
