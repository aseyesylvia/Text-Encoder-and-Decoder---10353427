"""Unit tests for the CipherLab algorithms.  Run:  python -m unittest -v"""
import unittest

from main import (ALGORITHMS, caesar_cipher, atbash_cipher, vigenere_cipher,
                  rail_fence_encode, base64_encode, morse_encode, xor_encode)


class TestAlgorithms(unittest.TestCase):
    def test_round_trip_every_algorithm(self):
        keys = {None: "", "shift": "5", "rails": "4", "text": "secret"}
        for name, info in ALGORITHMS.items():
            key = keys[info["key"]]
            text = "HELLO WORLD 123" if name == "Morse Code" else "Hello, World! 123"
            with self.subTest(algorithm=name):
                encoded = info["encode"](text, key)
                self.assertEqual(info["decode"](encoded, key).lower(), text.lower())

    def test_known_values(self):
        self.assertEqual(caesar_cipher("abc xyz", 3), "def abc")
        self.assertEqual(atbash_cipher("abc"), "zyx")
        self.assertEqual(vigenere_cipher("Hello", "key"), "Rijvs")
        self.assertEqual(rail_fence_encode("WEAREDISCOVERED", 3), "WECRERDSOEEAIVD")
        self.assertEqual(base64_encode("Hi"), "SGk=")
        self.assertEqual(morse_encode("SOS"), "... --- ...")
        self.assertEqual(xor_encode("A", "B"), "03")

    def test_bad_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            ALGORITHMS["Caesar Cipher"]["encode"]("hi", "abc")
        with self.assertRaises(ValueError):
            ALGORITHMS["Caesar Cipher"]["encode"]("hi", "40")
        with self.assertRaises(ValueError):
            ALGORITHMS["Base64"]["decode"]("not base64!", "")
        with self.assertRaises(ValueError):
            ALGORITHMS["Hexadecimal"]["decode"]("ZZ", "")
        with self.assertRaises(ValueError):
            ALGORITHMS["Binary"]["decode"]("102", "")
        with self.assertRaises(ValueError):
            ALGORITHMS["Vigenere Cipher"]["encode"]("hi", "123")
        with self.assertRaises(ValueError):
            ALGORITHMS["Morse Code"]["encode"]("hi #", "")


if __name__ == "__main__":
    unittest.main()
