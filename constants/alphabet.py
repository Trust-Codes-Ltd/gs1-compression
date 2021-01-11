"""safeBase64Alphabet is a modified URI-safe Base64 alphabet
 used in the compression methods for converting the binary string
  to/from an alphanumeric representation that contains no characters
  restricted in URIs."""
SAFE_BASE64_ALPHABET = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")

HEX_ALPHABET = "0123456789ABCDEF"
