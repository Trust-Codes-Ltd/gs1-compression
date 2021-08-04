import json
import logging
import traceback

from gs1.constants import AI_MAPS, AI_QUALIFIER
from gs1.utils import verify_check_digit, verify_syntax, element_strings_push

logger = logging.getLogger('__name__')


def populate_list(gs1_ai_array, key_name):
    return [a for a in gs1_ai_array.keys() if a in AI_MAPS.get(key_name)]


def build_gs1_element_strings(gs1_ai_array, brackets: bool):
    """
    this method converts an associative array of GS1 Application Identifiers
    and their values into concatenated GS1 element strings.
    set brackets=true if you want a human-readable concatenation with round
    brackets around GS1 Application Identifiers;
    set brackets=false if you don't; in this case the group separator will be
    used to mark the end of any field that is not defined length,
    except for the last element string in the concatenation.
    """
    # if brackets=true, use GS1 Digital Link ordering - identifier, qualifiers
    # then data attributes in numeric order
    element_strings = []
    identifiers = populate_list(gs1_ai_array, 'identifiers')
    qualifiers = populate_list(gs1_ai_array, 'qualifiers')
    attributes = populate_list(gs1_ai_array, 'dataAttributes')
    fixed_length_values = populate_list(gs1_ai_array, 'fixedLength')
    variable_length_values = populate_list(gs1_ai_array, 'variableLength')
    if brackets:
        if len(identifiers) != 1:
            logger.error('Stack trace:\n{}'.format(traceback.format_exc()))
            raise ValueError("The associative array should contain exactly one"
                             " primary identification key - it contained " +
                             str(len(identifiers)) + " " +
                             json.dumps(identifiers) +
                             "; please check for a syntax error")
        else:
            verify_syntax(identifiers[0], gs1_ai_array[identifiers[0]])
            verify_check_digit(identifiers[0], gs1_ai_array[identifiers[0]])
            element_strings = element_strings_push(
                element_strings, "(" + identifiers[0] + ")",
                gs1_ai_array[identifiers[0]], ""
            )
            if identifiers[0] in AI_QUALIFIER.keys():
                qualifiers_for_primary = AI_QUALIFIER[identifiers[0]]
                for key, value in qualifiers_for_primary:
                    if value in qualifiers:
                        element_strings = element_strings_push(
                            element_strings, "(" + value + ")",
                            gs1_ai_array[value], ""
                        )
            # append any found attributes to the elementStrings array
            sorted_attributes = sorted(attributes)
            for a in sorted_attributes:
                element_strings = element_strings_push(
                    element_strings, "(" + attributes[a] + ")",
                    gs1_ai_array[attributes[a]], ""
                )
    else:
        # if brackets=false, concatenate defined-length AIs first,
        # then variable-length AIs identify which AIs in gs1AIarray
        # are defined fixed length.
        fixed_length_primary_identifier = []
        fixed_length_values_other = fixed_length_values
        for i, value in enumerate(fixed_length_values_other):
            if value in identifiers:
                fixed_length_primary_identifier.append(value)
                fixed_length_values_other.pop(i)
        for i, value in enumerate(fixed_length_primary_identifier):
            element_strings = element_strings_push(
                element_strings, value, gs1_ai_array[value], "")
        for i, value in enumerate(fixed_length_values_other):
            element_strings = element_strings_push(
                element_strings, value, gs1_ai_array[value], "")
        for i, value in enumerate(variable_length_values):
            gs = ''
            if i < len(variable_length_values) - 1:
                gs = chr(29)
            element_strings = element_strings_push(
                element_strings, value, gs1_ai_array[value], gs)
    return ''.join(element_strings)
