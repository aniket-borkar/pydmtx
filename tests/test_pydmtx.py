import unittest
from pydmtx import encode, decode

class TestPyDMTX(unittest.TestCase):
    def test_encode_decode(self):
        data = "Hello World"
        matrix = encode(data)
        decoded = decode(matrix)
        self.assertEqual(decoded, data)

    def test_rs(self):
        from pydmtx.rs import rs_encode_msg, rs_correct_msg
        msg = [142, 164, 186]
        encoded = rs_encode_msg(msg, 5)
        self.assertEqual(encoded[3:], [114, 25, 5, 88, 102])
        decoded = rs_correct_msg(encoded, 5)
        self.assertEqual(decoded, msg)
        # Add error
        encoded[0] ^= 1  # Error
        decoded = rs_correct_msg(encoded, 5)
        self.assertEqual(decoded, msg)  # Corrected

if __name__ == '__main__':
    unittest.main()