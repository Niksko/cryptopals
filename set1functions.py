from base64 import b16decode, b64encode
from string import ascii_lowercase, ascii_letters

def hex_to_base64(inputString):
    """
    Converts hex to base 64 via binary using the base64 library
    Input: string in hex encoding
    Returns: string in base64 encoding
    """

    inputString = b16decode(inputString, casefold = True)
    return b64encode(inputString)

def fixed_XOR(string_one, string_two):
    """
    Takes two bytearrays of equal length and returns the result of XORing them
    Input: two bytearrays of equal length
    Returns: XORed result as bytearray
    Raises: ValueError if the bytearrays are not the same length
    """

    if len(string_one) != len(string_two):
        raise ValueError("Strings are not of the same length.")
    else:
        # Empty byte array
        retVal = bytearray()
        # Loop over the bytes in each string and xor them, then append them to our return value
        for i in range(len(string_one)):
            retVal.append(string_one[i] ^ string_two[i])

        # Return an immutable bytes object
        return bytes(retVal)


def english_plaintext_score(input_string):
    """
    Takes a piece of english plaintext and scores it based on letter frequency
    The score is based on the number of characters in the top 6 that appear in the english language top 6, and similarly
    for the 6 least common letters
    Input: a string in ascii encoding
    Return: a score as derived above
    """

    # input string to lower case
    input_string = input_string.lower()

    # Count the number of letters
    frequency_list = []
    for char in ascii_lowercase:
        frequency_list.append((char,input_string.count(char)))

    # Sort the list based on the occurance of each letter
    frequency_list.sort(key = lambda tuple: tuple[1], reverse = True)

    # Count the number of letters in the top six that appear in the english top six ETAOIN
    score = 0
    for i in range(6):
        if frequency_list[i][0] in "etaoin":
            score += 1

    # Count the number of letters in the last six that appear in the english last six VKJXQZ
    for i in range(20,26):
        if frequency_list[i][0] in "vkjxqz":
            score += 1

    # Subtract 1 for each non ascii character
    for char in input_string:
        if char not in ascii_letters:
            score -= 1

    return score


def single_byte_decipher(input_string):
    """
    Takes the input, XORs it with all possible single byte characters, ranks them based on MSE from english letter
    frequency, then returns a tuple of the byte with the lowest MSE, the MSE, and the plaintext
    Input: a bytestring ciphertext
    Returns: a tuple of the byte with the lowest MSE, the MSE and the plaintext as a byte string
    """
    MSE_list = []

    # Loop over all bytes
    for i in range(256):
        xor_bytes = bytes([i for _ in range(len(input_string))])
        try:
            xor_result = fixed_XOR(xor_bytes,input_string).decode("ascii")
            score = english_plaintext_score(xor_result)
            MSE_list.append((bytes([i]), score, xor_result))
        except UnicodeDecodeError:
            pass

    # Sort the list
    MSE_list.sort(key = lambda tuple: tuple[1], reverse = True)

    # Return the first tuple in the list
    return MSE_list[0]