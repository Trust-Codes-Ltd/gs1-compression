import logging
from urllib.parse import unquote

from decompress.binary_to_gs1_ai_array import decompress_binary_to_gs1_array
from decompress.analyse_uri import analyse_uri
from constants.regular_expressions import REGEX_ALL_NUM, REGEX_SAFE_64
from constants.path_sequence_constraints import PATH_SEQUENCE_CONSTRAINTS
from constants.ai_table import SHORT_CODE_TO_NUMERIC
from utils import base64_to_str, verify_check_digit, verify_syntax, pad_gtin


logger = logging.getLogger('__name__')


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
    obj_gs1 = {}
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
        if (not REGEX_ALL_NUM.match(key) and
                key not in SHORT_CODE_TO_NUMERIC.keys()):
            non_gs1_query_string_candidates[key] = obj_gs1[key]
            obj_gs1.pop(key)
    result['GS1'] = obj_gs1
    result['other'] = non_gs1_query_string_candidates
    return result
