from base64 import b16decode, b64encode

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

