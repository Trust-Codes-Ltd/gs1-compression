import re
import logging
import traceback

from gs1.utils import AI_BY_LENGTH
from gs1.constants import REGEX_ROUND_BRACKETS, REGEX_BRACKETED
from gs1.constants import AI_REGEX
from gs1.constants import FIXED_LENGTH_TABLE

logger = logging.getLogger('__name__')


def extract_from_element_strings(element_strings: str):
    """
    Extract GS1 application identifier from element strings.

    This method will convert either a bracketed element string or an unbracketed
    element string into an associative array.

    Input could be "(01)05412345000013(3103)000189(3923)2172(10)ABC123"
    or "3103000189010541234500001339232172"+groupSeparator+"10ABC123"
    """
    # remove symbology identifier if present
    # remove ]C1 or ]e0 or ]d2 or ]Q3
    element_strings = re.sub("^(]C1|]e0|]d2|]Q3)", '', element_strings)
    if REGEX_ROUND_BRACKETS.match(element_strings):
        ai_keys = AI_REGEX.keys()
        obj = {}
        k = ''
        if REGEX_BRACKETED.match(element_strings):
            results = re.findall(REGEX_BRACKETED, element_strings)
            for i, result in enumerate(results):
                if i % 2 == 0:
                    k = result[0]
                elif k in ai_keys:
                    if AI_REGEX[k].match(result[1]):
                        obj[k] = result[1]
                    else:
                        logger.error('Stack trace:\n{}'.format(
                            traceback.format_exc()))
                        raise ValueError(
                            "SYNTAX ERROR: invalid syntax for value of (" +
                            k + ") : " + result[1])
            return obj
    else:
        element_strings_length = len(element_strings)
        fixed_length_identifiers = FIXED_LENGTH_TABLE.keys()
        group_separator = chr(29)
        cursor = 0
        buffer = []
        while cursor < element_strings_length:
            first_two_digits = element_strings[cursor:cursor + 2]
            if first_two_digits in fixed_length_identifiers:
                # The first two digits are within the array of GS1
                # Application Identifiers of defined fixed length
                # extract the AI and value to the buffer
                length = FIXED_LENGTH_TABLE.get(first_two_digits)
                buffer.append(element_strings[cursor:cursor + length])
                cursor += length
                # If the next character is the group separator, move past
                if element_strings[cursor] == group_separator:
                    cursor += 1
            else:
                # The first two digits are not within the array of GS1
                # Application Identifiers of defined fixed length
                # if string contains group separator
                if group_separator in element_strings[cursor:]:
                    group_sep_loc = element_strings[cursor:].index(
                        group_separator)
                    buffer.append(element_strings[cursor:][0:group_sep_loc])
                    cursor += group_sep_loc
                    cursor += 1
                else:
                    buffer.append(element_strings[cursor:])
                    cursor = element_strings_length
        # Now process the buffer
        obj = {}
        matched = False
        for buffer_item in buffer:
            for k in [2, 3, 4]:
                ai_candidate = buffer_item[0:k]
                ai_sublist = [ai for ai in AI_BY_LENGTH if len(ai) == k]
                if ai_candidate in ai_sublist:
                    obj[ai_candidate] = buffer_item[k:]
                    matched = True
            if not matched:
                logger.error('Stack trace:\n{}'.format(traceback.format_exc()))
                raise ValueError("No matching GS1 AI found for " + buffer_item)
        return obj
