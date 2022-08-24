import sys
import numpy as np
from PIL import Image
import rsa

np.set_printoptions(threshold=sys.maxsize)


def encode(key_phrase, src, message, dest):
    """
    This function encodes text onto an image.
    str key_phrase : it indicates to the compiler where the end of the encoded message is
    str src : source image to utilize to encode message, must be png
    str message : message to encode onto an image
    str dest : name of the resulting image that contains the encoded message, must include .png at the end
    """
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    else:
        sys.exit("Not a compatible image. Try again")

    total_pixels = array.size // n
    if type(key_phrase) is bytes:
        key_phrase = key_phrase.decode('latin-1')
    message += key_phrase

    print(f'message before its transformed to binary {message}\n')
    # Transform to binary
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)
    print(f'Message in binary {b_message}')
    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index = 0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully.")
        return 0


def decode(src, key_phrase):
    """
    This function decodes the text hidden in an image.
    str src : the path of the image containing the encoded message, must be .png and include the extension
    str key_phrase : the phrase that indicates the end of the encoded message has been reached
    returns str encoded message
    """
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    else:
        sys.exit("There was a problem with the image. Try again.")

    total_pixels = array.size // n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

    #
    length_key = len(key_phrase)

    message = ""
    for i in range(len(hidden_bits)):
        if message[-length_key:] == key_phrase:
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if key_phrase in message:
        encoded_msg = message[:-length_key].encode('latin-1')
    else:
        encoded_msg = "No Hidden Message Found"
    return encoded_msg


def read_key_phrase(key_path):
    """
    Reads the key phrase from a txt file
    str key_path : path to the file containing the key phrase
    """
    try:
        with open(key_path, 'r') as f:
            lines = f.read()
            print("Key phrase loaded.\n")
    except NameError:
        print("File could not be found")
    return lines[:]


def read_encrypted_key_phrase(file_path):
    """Reads encrypted text and returns it as a string of bytes"""
    with open(file_path, mode='rb') as file:
        file_content = file.read()
        return file_content


def save_encrypted_key_phrase(file_path, encrypted_key_phrase):
    """Saves encrypted key phrase to a binary file"""
    with open(file_path, "wb") as binary_file:
        # Write bytes to file
        binary_file.write(encrypted_key_phrase)


def generate_rsa_key(n):
    """
    Generates public and private keys
    int n : key size
    returns public and private key
    """
    public_key, private_key = rsa.newkeys(n)
    return public_key, private_key


def rsa_encrypt(text, key):
    """Encrypts the given text with the passed key. Must be a byte string no longer than k--11 bytes,
    where k is the number of bytes needed to encode the n component of the key
    str text : text to encrypt
    key : must be a public key
    Returns the encrypted message as a string
    """
    message = text

    encrypted_message = rsa.encrypt(message.encode(), key)

    return encrypted_message


def load_private_key(private_key_file):
    """Loads private key from file.
    str private_key_file : path to pem or der file
    returns private key object
    """
    with open(private_key_file, mode='rb') as private_file:
        key_data = private_file.read()
    private_key = rsa.PrivateKey.load_pkcs1(key_data)

    return private_key


def load_public_key(public_key_file):
    """Loads public key from file.
    str private_key_file : path to pem or der file
    returns public key object
    """
    with open(public_key_file, mode='rb') as public_file:
        key_data = public_file.read()
    public_key = rsa.PublicKey.load_pkcs1(key_data)

    return public_key


def save_private_key(file_path, private_key):
    """Saves private key to specified file as a pem file"""
    with open(file_path, "wb") as f:
        f.write(private_key.save_pkcs1('PEM'))
    return 0


def save_public_key(file_path, public_key):
    """Saves public key to specified file as a pem file"""
    with open(file_path, "wb") as f:
        f.write(public_key.save_pkcs1('PEM'))
    return 0


def decrypt_with_private_key(private_key, encrypted_message):
    """Decrypts text with private key object"""
    decrypted_message = decrypted_message = rsa.decrypt(encrypted_message, private_key).decode()
    return decrypted_message


def decrypt_with_public_key(public_key, encrypted_message):
    """Decrypts text with public key object"""
    decrypted_message = decrypted_message = rsa.decrypt(encrypted_message, public_key).decode()
    return decrypted_message
