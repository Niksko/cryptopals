from base64 import b16decode, b64encode, b64decode
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
    try:
        return MSE_list[0]
    except IndexError:
        return (b'\xff', -1000000000, "")

def solveChallenge4():
    """
    Reads the challenge 4 ciphertext line by line, attempts to decipher it with the best single byte, then compares
    all of the plaintexts to find the one with the best score
    """
    plaintext_list = []
    i = -1

    with open("Challenge4.txt", 'r') as file:
        for line in file:
            i += 1
            plaintext_list.append((i, single_byte_decipher(b16decode(line.rstrip(), casefold = True))))

    plaintext_list.sort(key = lambda tuple: tuple[1][1], reverse = True)

    print(plaintext_list[0])

def repeating_key_XOR(plaintext, key):
    """
    Encodes a plaintext using a repeating key XOR function
    The first byte of the key is XORed with the first byte of the plaintext
    The second byte of the key is XORed with the second byte of the plaintext
    When the bytes in the key have been exhausted, you begin again with the first byte
    Input: plaintext as a bytes type
            key as a bytes type
    Returns: bytes of the XORed result
    """

    repeating_key = bytearray()

    # Convert the key into a repeating byte array of the same length as the plaintext
    key_length = len(key)
    plaintext_length = len(plaintext)
    for i in range(plaintext_length):
        key_byte = i % key_length
        repeating_key.append(key[key_byte])

    # XOR the repeating_key and the plaintext
    result = fixed_XOR(repeating_key, plaintext)

    return result


def hamming_distance(first_bytes, second_bytes):
    """
    Calculates the edit distance between two strings by finding the number of bits that are different
    Input: two strings of bytes
    Output: the number of bits difference between them
    """

    # XOR the two byte strings
    result = fixed_XOR(first_bytes, second_bytes)

    # Convert each byte to binary, and count the digits
    count = 0
    for byte in result:
        count += bin(byte).count("1")

    return count

def break_repeating_key_XOR(ciphertext):
    """
    Breaks repeating key XOR by first figuring out the most likely keysize, then transposing blocks of length keysize
    and breaking each using a single byte xor. Combining these results produces the most likely key
    Input: ciphertext as raw bytes
    Returns: tuple consisting of (key, plaintext)
    """

    # First, compute the most likely keysize
    keysize = compute_keysize(ciphertext, 2, 40, 4)

    # Next, split the ciphertext into blocks of size keysize
    block_array = []
    ciphertext_length = len(ciphertext)
    for i in range(ciphertext_length//keysize):
        block_array.append(ciphertext[i*keysize:(i+1)*keysize])

    # Transpose the blocks
    transposed_array = block_transpose(block_array)

    # Crack each transposed block using single byte XOR and put the keys together
    key = bytearray()
    for i in range(len(transposed_array)):
        key.append(ord(single_byte_decipher(transposed_array[i])[0]))

    # Decrypt the ciphertext using our key
    return (key, repeating_key_XOR(ciphertext, key))

def compute_keysize(ciphertext, smallest, largest, blocks):
    """
    Computes the probable keysize of a ciphertext by brute force. Take potential keysizes between smallest and largest,
    take the first <blocks> blocks of the ciphertext, find the hamming distance between adjacent blocks, then average
    the result and return the keysize with the smallest average
    Input: ciphertext as bytes
           smallest, largest and blocks as integers
    Returns: keysize as an integer
    """
    # Default values
    best_score = 10000000000
    keysize = largest + 1

    # For each potential keysize
    for potential_keysize in range(smallest, largest+1):

        # Set the score to 0
        score = 0
        # For each pair of blocks
        for i in range(blocks - 1):

            # Compute edit distance between adjacent blocks
            edit_distance = hamming_distance(ciphertext[i*potential_keysize:(i+1)*potential_keysize],
                                             ciphertext[(i+1)*potential_keysize:(i+2)*potential_keysize])
            # Add to the score, but normalise by keysize
            score += edit_distance / potential_keysize

        # Average all edit distances
        score /= (blocks - 1)

        # Update best keysize
        if score < best_score:
            keysize = potential_keysize
            best_score = score

    return keysize


def block_transpose(array):
    """
    Takes an array of byte blocks, and transposes them ie. take an array of n length m byte strings and generate
    an array of m length n byte strings by taking all of the first bytes, all of the second etc.
    Input: An array of byte strings
    Returns: That array transposed
    """
    # Initialise return value
    retVal = []

    # Loop based on the length of the first element in the array
    for i in range(len(array[0])):

        # Empty byte array to append onto
        byte_array = bytearray()

        # Loop over each element of the array
        for j in range(len(array)):
            # Append the byte to the bytearray
            byte_array.append(array[j][i])

        # Append to our return value
        retVal.append(byte_array)

    return retVal


def decode_b64_file(filename):
    """
    Takes a filename and returns the bytestring based on its contents, decoded as base 64
    Input: A filename to read from
    Returns: The contents of the file as a bytestring using base 64 decoding
    """

    with open(filename, 'r') as file:

        ciphertext = ""
        for line in file:
            ciphertext += line

    ciphertext = b64decode(ciphertext)

    return ciphertext
