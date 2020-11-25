import re

REGEX_ALL_NUM = re.compile("^[0-9]+$")
REGEX_HEX_LOWER = re.compile("^[0-9a-f]+$")
REGEX_HEX_UPPER = re.compile("^[0-9A-F]+$")
REGEX_SAFE_64 = re.compile("^[A-Za-z0-9_-]+$")

CHAR_TO_ESCAPE = "#/%&+,!()*':;<=>?"
