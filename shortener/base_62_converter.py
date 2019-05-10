import math

BASE = 62

UPPERCASE_OFFSET = 55
LOWERCASE_OFFSET = 61
DIGIT_OFFSET = 48


def true_ord(char):
    """
    Turns a digit [char] in character representation
    from the number system with base [BASE] into an integer.
    """

    ans = ord(char) - LOWERCASE_OFFSET
    if char.isdigit():
        ans = ord(char) - DIGIT_OFFSET
    elif 'A' <= char <= 'Z':
        ans = ord(char) - UPPERCASE_OFFSET

    return ans


def true_chr(integer):
    """
    Turns an integer [integer] into digit in base [BASE]
    as a character representation.
    """
    ans = chr(integer + LOWERCASE_OFFSET)
    if integer < 10:
        ans = chr(integer + DIGIT_OFFSET)
    elif 10 <= integer <= 35:
        ans = chr(integer + UPPERCASE_OFFSET)

    return ans


def saturate(key):
    """
    Turn the base [BASE] number [key] into an integer
    """
    int_sum = 0
    reversed_key = key[::-1]
    for idx, char in enumerate(reversed_key):
        int_sum += true_ord(char) * int(math.pow(BASE, idx))
    return int_sum


def dehydrate(num):
    if num == 0:
        return str(num)

    ans = ""
    while num > 0:
        remainder = num % BASE
        ans = true_chr(remainder) + ans
        num //= BASE
    return ans
