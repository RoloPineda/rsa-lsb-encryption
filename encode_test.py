import unittest

from Stego import Decode, read_encryption_key, rsa_encrypt, save_private_key, rsa_decrypt, Encode


class Stego(unittest.TestCase):
    def test_encode(self):
        self.assertEqual(Decode("./testing/testkey.png", "$J@NcRfUjXn2r5u8x"), "No Hidden Message Found")  # add assertion here
        self.assertEqual(Decode("./testing/unittest2.png", "$lmfaodude"), "I love you")


    def test_read_encryption_key(self):
        self.assertEqual(read_encryption_key("./testing/key.txt"), '$J@NcRfUjXn2r5u8x')
        self.assertEqual(read_encryption_key("./testing/testkey1.txt"), '$mfklamsfklasfaafsd')

    def test_rsa_encrypt_decrypt(self):
        public_key, private_key, encrypted_message = rsa_encrypt("Hello there")
        file_path = "./testing/key1test.pem"
        save_private_key(file_path, private_key)

        self.assertEqual(rsa_decrypt(file_path, encrypted_message), "Hello there")

    def test_encrypt_message_lsb(self):
        message = "hello there"
        src = "surfer_in_barrel.png"
        encryption_key = "$lmfao"
        file_private_key = "./testing/rsa-lsb.pem"
        public_key, private_key, encrypted_message = rsa_encrypt("Hello there")
        save_private_key(file_private_key, private_key)
        dest = "./testing/rsa-lsb.png"


        Encode(encryption_key, src, encrypted_message, dest)

        self.assertEqual(Decode(dest, encryption_key, 2), encrypted_message)

if __name__ == '__main__':
    unittest.main()
