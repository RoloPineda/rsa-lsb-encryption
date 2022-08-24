# rsa-lsb-encryption
<pre>
This program encrypts text to an image using LSB.

An example workflow for encoding a text would be:

1). Create a key phrase and store it in a .txt file for the program to read.
2). Call the read_key_phrase function to load it onto a string that can be called.
  2.1). Generate private or public keys to encrypt the key phrase depending on the needs
  2.2). Save the keys to corresponding files
3). Encrypt key phrase
4). Store encrypted key phrase in a binary file to send to recipient
5). Encode text onto the image

Image before encoding:
<img src="https://github.com/RoloPineda/rsa-lsb-encryption/blob/master/encoding_example/surfer_in_barrel.png" width=400 height=300>

Image after encoding:
<img src="https://github.com/RoloPineda/rsa-lsb-encryption/blob/master/encoding_example/image_with_encoded_text.png" width=400 height=300>

See encoding_example\encode.py 

An example workflow for decoding text would be:

1). Load encrypted key phrase
2). Decrypt it with private key
3). Decode text from image


</pre>
