import unittest

from set1functions import *

class Test_Set1(unittest.TestCase):
    """
    Tests the functions in set 1 of the cryptopals challenge
    """

    def test_hex_to_64(self):
        """Tests the hex to base 64 function on the input provided"""
        test_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        correct_string = b'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
        self.assertEqual(hex_to_base64(test_string), correct_string)

    def test_XOR_uneven_length(self):
        """Tests that the XOR function raises an error for bytestrings of uneven length"""
        string_one = b16decode("AF")
        string_two = b16decode("AFAF")
        self.assertRaises(ValueError, fixed_XOR, string_one, string_two)

    def test_XOR_valid(self):
        """Tests that the XOR function works for the values provided to us"""
        string_one = b16decode("1c0111001f010100061a024b53535009181c", casefold = True)
        string_two = b16decode("686974207468652062756c6c277320657965", casefold = True)
        result = fixed_XOR(string_one, string_two)
        expectedResult = b16decode("746865206b696420646f6e277420706c6179", casefold = True)
        self.assertEqual(result, expectedResult)
