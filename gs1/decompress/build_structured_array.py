import json
import logging
import traceback

from gs1.constants import AI_MAPS
from gs1.utils import verify_syntax, verify_check_digit

logger = logging.getLogger('__name__')


def build_structured_array(gs1_ai_array, other_array):
    """
    New method that converts a flat associative array of GS1 Application
    Identifiers and their values into a more structured object in which
    the primary identification key, key qualifiers, data attributes and
    other key=value pairs from the URI string are clearly identified as such.
    """
    keys = ["identifiers", "qualifiers", "dataAttributes"]
    result = {
        'identifiers': [],
        'qualifiers': [],
        'dataAttributes': [],
        'other': [],
    }
    for key, value in gs1_ai_array.items():
        b = {key: value}
        other = True
        for key_ in keys:
            if key in AI_MAPS.get(key_):
                result[key_].append(b)
                other = False
        if other:
            result['other'].append(b)
    for key, value in other_array.items():
        b = {key: value}
        result['other'].append(b)
    if len(result.get('identifiers')) != 1:
        logger.error('Stack trace:\n{}'.format(traceback.format_exc()))
        raise ValueError("The element string should contain exactly one primary"
                         " identification key - it contained " +
                         str(len(result['identifiers'])) + " " +
                         json.dumps(result['identifiers']) +
                         "; please check for a syntax error")
    else:
        result_key = list(result['identifiers'][0].keys())
        result_value = list(result['identifiers'][0].values())
        verify_syntax(result_key[0], result_value[0])
        verify_check_digit(result_key[0], result_value[0])
    return result
