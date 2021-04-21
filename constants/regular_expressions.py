import re

REGEX_ALL_NUM = re.compile("^[0-9]+$")
REGEX_HEX_LOWER = re.compile("^[0-9a-f]+$")
REGEX_HEX_UPPER = re.compile("^[0-9A-F]+$")
REGEX_SAFE_64 = re.compile("^[A-Za-z0-9_-]+$")

# The regex to check if an initial application identifier is enclosed within
# round brackets.
REGEX_ROUND_BRACKETS = re.compile("^\\((\\d{2,4}?)\\)")
REGEX_BRACKETED = re.compile("\\((\\d{2,4}?)\\)|([^(]+)")

CHAR_TO_ESCAPE = "#/%&+,!()*':;<=>?"
