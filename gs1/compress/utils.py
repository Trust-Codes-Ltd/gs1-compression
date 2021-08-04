from gs1.constants import TABLE_OPT
from gs1.constants import AI_MAPS


def find_candidates_from_table_opt(key_list, table_opt=TABLE_OPT):
    """
    Get a candidate dict from a key list and the OPT table.
    :param key_list: key list.
    :param table_opt: optimized encoding table.
    :return: Candidate dictionary.
    """
    existence_list = {key: len(''.join(TABLE_OPT[key]))
                      for key, value in table_opt.items()
                      if set(value).issubset(set(key_list))
                      }
    return existence_list


def find_best_optimization_candidate(candidates_from_table_opt):
    """

    :param candidates_from_table_opt:
    :return:
    """
    max_key = ''
    max_threshold = 0
    for key, value in candidates_from_table_opt.items():
        if value > max_threshold:
            max_key = key
            max_threshold = value
    return max_key


def remove_optimized_key_from_ai_list(key_list: list, optimized_dict: dict):
    """

    :param key_list:
    :param optimized_dict:
    :return:
    """
    for key, value in optimized_dict.items():
        if value in key_list:
            ind = key_list.index(value)
            key_list.pop(ind)
    return key_list


def separate_id_non_id(gs1_ai_array):
    """
    Separate the identifiers from non-identifiers in a GS1 application
    identifier array.

    :param gs1_ai_array: GS1 application identifier array.
    :return: A dict object with separate parts of the array.
    """
    result = {}
    id_array = {}
    non_id_array = {}
    for key in gs1_ai_array.keys():
        if key in AI_MAPS.get('identifiers'):
            id_array[key] = gs1_ai_array.get(key)
        else:
            non_id_array[key] = gs1_ai_array.get(key)
    result['ID'] = id_array
    result['nonID'] = non_id_array
    return result
