import unittest

from set1functions import *

class Test_Set1(unittest.TestCase):
    """
    Tests the functions in set 1 of the cryptopals challenge
    """

    def test_hex_to_64(self):
        """Tests the hex to base 64 function on the input provided"""
        test_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        correct_string = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        self.assertEqual(hex_to_base64(test_string), correct_string)
