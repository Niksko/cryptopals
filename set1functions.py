from base64 import b16decode, b64encode
from string import ascii_lowercase

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
    The frequency of each letter is computed, and then the mean squared deviation between english frequencies and
    measured frequencies is computed
    Input: a string in ascii encoding
    Returns: the means squared deviation between the letter frequency in the plaintext and the english letter frequency
    Raises: ValueError if the list returned from the frequency file conversion doesn't have 26 elements
    """

    # English letter frequencies in alphabetical order
    english_frequencies = frequencies_to_list("english_frequencies.txt")

    if len(english_frequencies) != 26:
        raise ValueError("English frequencies list does not contain an entry for each letter")

    # input string to lower case
    input_string = input_string.lower()

    # Calculate plaintext frequencies for each letter in the plaintext
    plaintext_frequencies = []
    string_length = len(input_string)
    for char in ascii_lowercase:
        char_count = input_string.count(char)
        plaintext_frequencies.append(char_count/string_length)

    # Compute the MSE
    MSE = 0
    for i in range(26):
        MSE += (plaintext_frequencies[i] - english_frequencies[i]) ** 2

    MSE /= 26
    return MSE


def frequencies_to_list(input_file):
    """
    Reads letter frequencies from a file and converts them to a list
    Assumes that the frequencies in the file are ordered from a to z
    Input: filename of frequency table to import
    Returns: list of all of the lines in the file converted to floats
    """

    retVal = []

    with open(input_file, 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            retVal.append(float(line))

    return retVal
