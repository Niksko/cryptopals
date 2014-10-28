from base64 import b16decode, b64encode

def hex_to_base64(inputString):
    """
    Converts hex to base 64 via binary using the base64 library
    Input: string in hex encoding
    Returns: string in base64 encoding
    """

    inputString = b16decode(inputString, casefold = True)
    return b64encode(inputString)