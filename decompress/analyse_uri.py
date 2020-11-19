from urllib.parse import unquote

from constants.regular_expressions import REGEX_ALL_NUM, REGEX_SAFE_64
from constants.ai_table import SHORT_CODE_TO_NUMERIC, AI_MAPS, AI_REGEX
from decompress.extract import (extract_from_compressed_gs1_digital_link,
                                extract_from_gs1_digital_link)
from decompress.build_structured_array import build_structured_array
from decompress.build_gs1_element_strings import (
    gs1_digital_link_to_gs1_element_strings,
    gs1_compressed_digital_link_to_gs1_element_strings)


def analyse_uri(gs1_digital_link_uri, extended: bool) -> dict:
    """"""
    result = {
        'fragment': '',
        'queryString': '',
        'pathComponents': '',
        'detected': '',
        'uncompressedPath': '',
        'compressedPath': '',
        'structuredOutput': '',
    }
    hash_index = gs1_digital_link_uri.index('#')
    before_fragment = gs1_digital_link_uri
    if hash_index < len(gs1_digital_link_uri) - 1:
        result['fragment'] = gs1_digital_link_uri[1 + hash_index:]
        before_fragment = gs1_digital_link_uri[:hash_index]
    before_query_string = before_fragment
    question_index = before_fragment.index('?')
    if question_index < len(before_fragment) - 1:
        result['queryString'] = before_fragment[1 + question_index:]
        before_query_string = before_fragment[:question_index]
    # discard any trailing forward slash
    if before_query_string[-1] == '/':
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
    pc_length = len(path_components)
    pc_i = pc_length
    searching = True
    numeric_primary_identifier = ""
    for i, comp in enumerate(path_comp_reverse):
        if REGEX_ALL_NUM.match(comp):
            num_key = comp
        else:
            num_key = SHORT_CODE_TO_NUMERIC.get(comp, '')
        if num_key and searching:
            num_key_index = AI_MAPS.get('identifiers').index(num_key)
            if num_key_index < len(AI_MAPS.get('identifiers')):
                searching = False
                pc_i = pc_length - i
                numeric_primary_identifier = num_key
                relevant_path_components = path_comp_reverse[:i + 1][::-1]
                uri_stem_path_components = path_comp_reverse[: i + 2][::-1]
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
