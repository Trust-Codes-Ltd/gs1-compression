from gs1.constants import SHORT_CODE_TO_NUMERIC


def deal_with_duplicates(gs1_array: dict):
    """Final check before building the original digital link."""
    keys = gs1_array.keys()
    short_code_keys = [key for key in keys
                       if key in SHORT_CODE_TO_NUMERIC.keys()]
    if short_code_keys:
        for short_code in short_code_keys:
            value = gs1_array.get(short_code)
            gs1_array.pop(short_code)
            gs1_array.update({SHORT_CODE_TO_NUMERIC.get(short_code): value})
    return gs1_array
