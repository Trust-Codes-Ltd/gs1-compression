import re
import logging
from urllib.parse import unquote

from constants.regular_expressions import REGEX_ALL_NUM, REGEX_SAFE_64
from constants.ai_table import SHORT_CODE_TO_NUMERIC, AI_MAPS, AI_REGEX
from constants.path_sequence_constraints import PATH_SEQUENCE_CONSTRAINTS

from gs1.decompress.build_structured_array import build_structured_array
from gs1.decompress.build_gs1_element_strings import build_gs1_element_strings
from gs1.decompress.binary_to_gs1_ai_array import decompress_binary_to_gs1_array
from gs1.utils import base64_to_str, verify_check_digit, verify_syntax, pad_gtin

logger = logging.getLogger('__name__')


def gs1_digital_link_to_gs1_element_strings(digital_link_uri, brackets):
    """translate a GS1 Digital Link URI into
    a string of concatenated GS1 element strings
    """
    return build_gs1_element_strings(
        extract_from_gs1_digital_link(digital_link_uri).get('GS1'), brackets)


def gs1_compressed_digital_link_to_gs1_element_strings(
        digital_link_uri, brackets):
    """
    Translate a compressed GS1 Digital Link URI into a string of
    concatenated GS1 element strings.
    """
    return build_gs1_element_strings(
        extract_from_compressed_gs1_digital_link(
            digital_link_uri).get('GS1'), brackets)


def extract_from_gs1_digital_link(gs1_digital_link_uri):
    """this method converts a GS1 Digital Link URI into an
    associative array of GS1 Application Identifiers and their values.
    """
    obj_gs1 = {}
    result = {}

    # Extract path info and query string from URI and parse
    # the result as a dictionary.
    analyse_result = analyse_uri(gs1_digital_link_uri, extended=False)
    uri_path_info = analyse_result.get('uriPathInfo')
    path_candidates = analyse_result.get('pathCandidates')
    split_path = uri_path_info.split('/')[1:]
    ai_sequence = [
        SHORT_CODE_TO_NUMERIC[split_path[i]]
        for i in reversed(range(len(split_path)))
        if i % 2 == 0 and REGEX_ALL_NUM.match(split_path[i])
    ]
    ai_sequence = ai_sequence[::-1]

    # check that the URI path components appear in the correct sequence.
    if ai_sequence[0] in PATH_SEQUENCE_CONSTRAINTS.keys():
        last_index = -1
        for j in range(1, len(ai_sequence)):
            if (ai_sequence[j] not in
                    PATH_SEQUENCE_CONSTRAINTS[ai_sequence[0]] or
                    PATH_SEQUENCE_CONSTRAINTS[ai_sequence[0]].index(ai_sequence[j]) <= last_index
            ):
                raise Exception("Invalid GS1 Digital Link - invalid sequence"
                                " of key qualifiers found in URI path"
                                " information.")
            last_index = PATH_SEQUENCE_CONSTRAINTS[
                ai_sequence[0]].index(ai_sequence[j])
    # log the number keys
    for key in path_candidates.keys():
        if not REGEX_ALL_NUM.match(key):
            logger.info("numkey = {}".format(key))
    query_string_candidates = analyse_result.get('queryStringCandidates')
    non_gs1_query_string_candidates = {}

    # Merge path_candidates and query_string_candidates into
    # a combined associative array - candidates.
    candidates = path_candidates.update(query_string_candidates)
    for key, value in candidates.items():
        if not REGEX_ALL_NUM.match(key):
            # For keys that are not all-numeric,
            # attempt to convert to all-numeric AI equivalent.
            if key in SHORT_CODE_TO_NUMERIC.keys():
                num_key = SHORT_CODE_TO_NUMERIC[key]
                candidates[num_key] = candidates[key]
            else:
                # Otherwise remove from candidates map if
                # it doesn't relate to a GS1 Application Identifier.
                non_gs1_query_string_candidates[key] = candidates[key]
            candidates.pop(key)

    # Check that each entry in the associative array has the correct syntax
    # and correct digit (where appropriate).
    for key, value in candidates.items():
        verify_syntax(key, value)
        verify_check_digit(key, value)
        obj_gs1[key] = pad_gtin(key, value)
    result['GS1'] = obj_gs1
    result['other'] = non_gs1_query_string_candidates
    return result


def extract_from_compressed_gs1_digital_link(gs1_digital_link_uri):
    """this method converts a compressed GS1 Digital Link URI into an
    associative array of GS1 Application Identifiers and their values.
    """
    result = {}

    # set cursor to 0 - start reading from the left-most part of the
    # gs1 Digital Link URI as input.
    analyse_result = analyse_uri(gs1_digital_link_uri, extended=False)
    query_string = analyse_result.get('queryString')
    uri_path_info = analyse_result.get('uriPathInfo')
    non_gs1_query_string_candidates = {}
    if query_string:
        # if semicolon was used as delimiter between key=value pairs,
        # replace with ampersand as delimiter
        query_string = query_string.replace(';', '&')
        if '#' in query_string:
            first_fragment = query_string.index('#')
            query_string = query_string[:first_fragment]
        pairs = query_string.split('&')
        for pair in pairs:
            separate_by_equal = pair.split('=')
            if (separate_by_equal[0] and
                    separate_by_equal[1] and
                    not REGEX_ALL_NUM.match(separate_by_equal[0]) and
                    not separate_by_equal[0] in SHORT_CODE_TO_NUMERIC):
                non_gs1_query_string_candidates.update(
                    {separate_by_equal[0]: unquote(separate_by_equal[1])}
                )
    uri_path_info = uri_path_info[1:]
    if REGEX_SAFE_64.match(uri_path_info):
        binary_str = base64_to_str(uri_path_info)
        obj_gs1 = decompress_binary_to_gs1_array(binary_str)
    else:
        first_index = uri_path_info.index("/")
        last_index = uri_path_info.rindex("/")
        gs1_primary_key = uri_path_info[:first_index]
        base64_segment = uri_path_info[1 + last_index:]
        gs1_primary_key_value = uri_path_info[1 + first_index:last_index]
        obj_gs1 = decompress_binary_to_gs1_array(base64_to_str(base64_segment))
        if REGEX_ALL_NUM.match(gs1_primary_key):
            obj_gs1[gs1_primary_key] = gs1_primary_key_value
        elif gs1_primary_key in SHORT_CODE_TO_NUMERIC.keys():
            obj_gs1[
                SHORT_CODE_TO_NUMERIC[gs1_primary_key]] = gs1_primary_key_value

    # insert into associative array return value any key=value pairs
    # from the URI query string that were not compressed

    for key in obj_gs1.keys():
        if (not re.match(REGEX_ALL_NUM, key) and
                key not in SHORT_CODE_TO_NUMERIC.keys()):
            non_gs1_query_string_candidates[key] = obj_gs1[key]
    for key in non_gs1_query_string_candidates.keys():
        obj_gs1.pop(key)
    result['GS1'] = obj_gs1
    result['other'] = non_gs1_query_string_candidates
    return result


def analyse_uri(gs1_digital_link_uri: str, extended: bool) -> dict:
    """Analyze the compressed URI."""
    result = {
        'fragment': '',
        'queryString': '',
        'pathComponents': '',
        'detected': '',
        'uncompressedPath': '',
        'compressedPath': '',
        'structuredOutput': '',
    }
    before_fragment = gs1_digital_link_uri
    if '#' in gs1_digital_link_uri:
        hash_index = gs1_digital_link_uri.index('#')
        result['fragment'] = gs1_digital_link_uri[1 + hash_index:]
        before_fragment = gs1_digital_link_uri[:hash_index]
    before_query_string = before_fragment

    if '?' in before_fragment:
        question_index = before_fragment.index('?')
        result['queryString'] = before_fragment[1 + question_index:]
        before_query_string = before_fragment[:question_index]
    # discard any trailing forward slash
    if before_query_string.endswith('/'):
        before_query_string = before_query_string[:-1]
    cursor = 0
    if before_query_string.startswith("http://"):
        cursor = 7
    if before_query_string.startswith("https://"):
        cursor = 8
    protocol = before_query_string[:cursor]
    after_protocol = before_query_string[cursor:]
    first_slash_of_all_path = after_protocol.index('/')
    path_info = after_protocol[1 + first_slash_of_all_path:]
    result['uriPathInfo'] = '/' + path_info
    domain = after_protocol[:first_slash_of_all_path]
    path_components = path_info.split('/')

    # iterate through pathComponents to find the path component
    # corresponding to a primary GS1 ID key
    relevant_path_components = []
    uri_stem_path_components = []
    path_comp_reverse = path_components[::-1]
    searching = True
    numeric_primary_identifier = ""
    for i, comp in enumerate(path_comp_reverse):
        if REGEX_ALL_NUM.match(comp):
            num_key = comp
        else:
            num_key = SHORT_CODE_TO_NUMERIC.get(comp, '')
        if num_key and searching:
            if num_key in AI_MAPS.get('identifiers'):
                searching = False
                numeric_primary_identifier = num_key
                relevant_path_components = path_comp_reverse[:i + 1][::-1]
                uri_stem_path_components = path_comp_reverse[i + 1:][::-1]
    if len(relevant_path_components) > 0:
        result['pathComponents'] = '/' + '/'.join(relevant_path_components)
    if len(uri_stem_path_components) > 0:
        result['uriStem'] = (
                protocol + domain + '/' + '/'.join(uri_stem_path_components))
    else:
        result['uriStem'] = protocol + domain

    # if semicolon was used as delimiter between key=value pairs,
    # replace with ampersand as delimiter
    result['queryString'] = result.get('queryString').replace(';', '&')

    # process URI path information
    path_candidates = {}
    path_elements = relevant_path_components
    length_path_elements = len(path_elements)
    path_element_index = length_path_elements - 2
    while path_element_index >= 0:
        path_candidates[path_elements[path_element_index]] = unquote(
            path_elements[1 + path_element_index])
        path_element_index -= 2

    query_string_candidates = {}
    if result.get('queryString'):
        pairs = result.get('queryString').split('&')
        split_pairs = [pair.split('=') for pair in pairs]
        for p in split_pairs:
            if p[0] and p[1]:
                if p[0] in SHORT_CODE_TO_NUMERIC.keys():
                    query_string_candidates[
                        SHORT_CODE_TO_NUMERIC[p[0]]] = unquote(p[1])
                else:
                    query_string_candidates[p[0]] = unquote(p[1])
    result['pathCandidates'] = path_candidates
    result['queryStringCandidates'] = query_string_candidates
    if (len(relevant_path_components) > 0 and
            len(relevant_path_components) % 2 == 0):
        if AI_REGEX.get(numeric_primary_identifier).match(
                relevant_path_components[1]):
            result['detected'] = 'uncompressed GS1 Digital Link'
            result['uncompressedPath'] = '/' + '/'.join(
                relevant_path_components)
            if extended:
                extracted = extract_from_gs1_digital_link(gs1_digital_link_uri)
                gs1_array = extracted.get('GS1')
                other_array = extracted.get('other')
                result['structuredOutput'] = build_structured_array(
                    gs1_array, other_array)
                result['elementStringsOutput'] = gs1_digital_link_to_gs1_element_strings(
                    gs1_digital_link_uri, brackets=True)
    if (len(relevant_path_components) == 3 and
            REGEX_SAFE_64.match(relevant_path_components[2])):
        if AI_REGEX.get(numeric_primary_identifier).match(
                relevant_path_components[1]):
            result['detected'] = 'partially compressed GS1 Digital Link'
            result['uncompressedPath'] = '/' + '/'.join(
                relevant_path_components[:2])
            result['compressedPath'] = relevant_path_components[2]
            if extended:
                extracted = extract_from_compressed_gs1_digital_link(
                    gs1_digital_link_uri)
                gs1_array = extracted.get('GS1')
                other_array = extracted.get('other')
                result['structuredOutput'] = build_structured_array(
                    gs1_array, other_array)
                result['elementStringsOutput'] = gs1_compressed_digital_link_to_gs1_element_strings(
                    gs1_digital_link_uri, brackets=True)
    if (not result.get('detected') and
            REGEX_SAFE_64.match(path_comp_reverse[0]) and protocol):
        result['detected'] = "fully compressed GS1 Digital Link"
        result['compressedPath'] = path_comp_reverse[0]
        if extended:
            extracted = extract_from_compressed_gs1_digital_link(
                gs1_digital_link_uri)
            gs1_array = extracted.get('GS1')
            other_array = extracted.get('other')
            result['structuredOutput'] = build_structured_array(
                gs1_array, other_array)
            result['elementStringsOutput'] = gs1_compressed_digital_link_to_gs1_element_strings(
                gs1_digital_link_uri, brackets=True)
    return result
