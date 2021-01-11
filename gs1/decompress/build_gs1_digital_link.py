import json

from gs1.decompress.build_gs1_element_strings import populate_list
from constants.ai_table import AI_UNION_KEYS, AI_SHORT_CODE, AI_QUALIFIER
from gs1.utils import verify_syntax, verify_check_digit, percent_encode


def build_gs1_digital_link(
        gs1_ai_array,
        use_short_text,
        uri_stem: str,
        non_gs1_key_value_pairs
):
    """
    This method converts an associative array of GS1 Application Identifiers and
    their values into a GS1 Digital Link URI.
    Set useShortText = true if you wish to use alphabetic mnemonic short names,
    e.g. /gtin/ instead of /01/.
    Set uriStem to a value e.g. 'https://example.org' if you wish to use a
    specific domain name; set uriStem to null, undefined or "" defaults to
    'https://id.gs1.org' as the reference domain.

    :param gs1_ai_array: An array of application identifiers.
    :param use_short_text: Boolean variable. See the comments above.
    :param uri_stem: Domain name. See the comments above.
    :param non_gs1_key_value_pairs:
    :return: Reconstructed digital link.
    """
    path = ""
    query_string = ""
    query_string_array = []
    canonical_stem = "https://id.gs1.org"
    if uri_stem and uri_stem.endswith('/'):
        uri_stem = ''.join([uri_stem[:-1], path, query_string])
    identifiers = populate_list(gs1_ai_array, 'identifiers')
    qualifiers = populate_list(gs1_ai_array, 'qualifiers')
    attributes = populate_list(gs1_ai_array, 'dataAttributes')
    other_keys = [a for a in gs1_ai_array.keys() if a not in AI_UNION_KEYS]

    if len(identifiers) != 1:
        valid = False
        raise Exception("The element string should contain exactly one"
                        " primary identification key - it contained " +
                        str(len(identifiers)) + " " + json.dumps(identifiers) +
                        "; please check for a syntax error")
    else:
        verify_syntax(identifiers[0], gs1_ai_array[identifiers[0]])
        verify_check_digit(identifiers[0], gs1_ai_array[identifiers[0]])
        if use_short_text:
            if AI_SHORT_CODE.get(identifiers[0]):
                path = ''.join(['/', AI_SHORT_CODE.get(identifiers[0]),
                                '/', percent_encode(gs1_ai_array[identifiers[0]])])
            else:
                path = ''.join(['/', identifiers[0], '/',
                                percent_encode(gs1_ai_array[identifiers[0]])])
        else:
            path = ''.join(['/', identifiers[0], '/',
                            percent_encode(gs1_ai_array[identifiers[0]])])
        if AI_QUALIFIER.get(identifiers[0]):
            for value in AI_QUALIFIER.get(identifiers[0]):
                if value in qualifiers:
                    if use_short_text:
                        if AI_SHORT_CODE.get(value):
                            path += ''.join(
                                ['/', AI_SHORT_CODE.get(value),
                                 '/', percent_encode(gs1_ai_array[value])])
                        else:
                            path += ''.join(['/', value, '/',
                                            percent_encode(gs1_ai_array[value])])
                    else:
                        path += ''.join(['/', value, '/',
                                        percent_encode(gs1_ai_array[value])])
        if len(attributes) > 0:
            for key in attributes:
                if use_short_text:
                    if AI_SHORT_CODE.get(key):
                        query_string_array.append(
                            ''.join([AI_SHORT_CODE.get(key), '=',
                                     percent_encode(gs1_ai_array[key])]))
                    else:
                        query_string_array.append(
                            ''.join([key, '=',
                                     percent_encode(gs1_ai_array[key])]))
                else:
                    query_string_array.append(
                        ''.join([key, '=',
                                 percent_encode(gs1_ai_array[key])]))
            query_string = ''.join(['?', '&'.join(query_string_array)])

        if not uri_stem:
            web_uri = canonical_stem + path + query_string
        else:
            web_uri = uri_stem + path + query_string
        if len(other_keys) > 0:
            query_string_array = [''.join([key, '=',
                                           gs1_ai_array[key]])
                                  for key in other_keys]
            if query_string == '':
                web_uri += ''.join(['?', '&'.join(query_string_array)])
            else:
                web_uri += ''.join(['&', '&'.join(query_string_array)])
        if non_gs1_key_value_pairs:
            query_string_array = [
                ''.join([key, '=', value])
                for key, value in non_gs1_key_value_pairs.items()
            ]
            if query_string == '':
                web_uri += ''.join(['?', '&'.join(query_string_array)])
            else:
                web_uri += ''.join(['&', '&'.join(query_string_array)])
        return web_uri
