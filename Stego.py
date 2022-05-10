import sys
import numpy as np
from PIL import Image
import rsa


np.set_printoptions(threshold=sys.maxsize)

# encoding function
def Encode(encryption_key, src, message, dest):

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    else:
        sys.exit("Not a compatible image. Try again")

    total_pixels = array.size//n
    if type(message) == bytes:
        message = message.decode('latin-1')
    message += encryption_key

    # Transform to binary
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index=0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully.")
        return 0

# decoding function
def Decode(src, encryption_key, layers):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    else:
        sys.exit("There was a problem with the image. Try again.")

    total_pixels = array.size//n


    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]
    length_key = len(encryption_key)
    message = ""
    for i in range(len(hidden_bits)):
        if message[-length_key:] == encryption_key:
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if encryption_key in message:
        #print("Hidden Message:", message[:-length_key])

        encoded_msg = message[:-length_key].encode('latin-1')
        return encoded_msg

    else:
        #print("No Hidden Message Found")
        return "No Hidden Message Found"

def read_encryption_key(key_path):
    try:
        with open(key_path, 'r') as f:
            lines = f.read()
            print("Key Loaded.\n\n")
        return lines[:]
    except NameError:
        print("File could not be found")
    except:
        print("Something else went wrong")


def rsa_encrypt(text):
    message = text
    public_key, private_key = rsa.newkeys(512)
    encrypted_message = rsa.encrypt(message.encode(), public_key)
    #print("Original message: {}".format(message))
    #print("Encrypted message: {}".format(encrypted_message))

    #decrypted_message = rsa.decrypt(encrypted_message, private_key).decode()
    #print("Decoded: {}".format(decrypted_message))
    return public_key, private_key, encrypted_message


def rsa_decrypt(private_key_file, encrypted_message):
    with open(private_key_file, mode='rb') as privatefile:
        keydata = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
    decrypted_message = decrypted_message = rsa.decrypt(encrypted_message, privkey).decode()
    return decrypted_message


def save_private_key(file_path, private_key):
    """Saves private key object to specified file with a .pem extension"""
    f = open(file_path, "wb")
    f.write(private_key.save_pkcs1('PEM'))
    f.close()
    return 0

# main function
def Stego():
    print("--Welcome to your LSB Encryption program--")
    print("Enter 1 to Encode")
    print("Enter 2 to Decode")
    func = input()

    if func == '1':
        layers = int(input("Enter 1 or 2 to choose layers of encryption: "))
        if layers == 1:
            print("Enter Source Image Path")
            src = input()
            print("Enter Message to Hide")
            message = input()
            print("Enter name of output image")
            dest = input()
            print("Would you like to: ")
            print("1. Provide your own encryption key")
            print("2. Read from a file")
            encryption_in_file = int(input())

            # if user wants to provide own encryption
            if encryption_in_file == 1:
                encryption_key = input("Enter your encryption key: ")

            # if user wants to read from file
            elif encryption_in_file == 2:
                file = str(input("Provide the file where your key is located including the extension: "))
                encryption_key = read_encryption_key(file)
            else:
                SystemExit("No valid choice provided")
            print("Encoding...")
            Encode(encryption_key, src, message, dest)

        elif layers == 2:
            print("Enter Source Image Path")
            src = input()
            print("Enter Message to Hide")
            message = input()
            print("Enter name of output image")
            dest = input()

            # Applying rsa encryption to message and saving key to reuse later
            print("Applying RSA encryption to message ")
            public_key, private_key, encrypted_message = rsa_encrypt(message)
            print("...")
            print("Moving on to saving private key...")

            # Getting file name from user
            file_name = input("Enter the file name with extension pem: ")
            save_private_key(file_name, private_key)

            # Getting LSB encryption key
            print("Done with RSA encryption.")
            print()
            print("---LSB Key---")
            print("Would you like to: ")
            print("1. Provide your own encryption key")
            print("2. Read key from a file: ")
            encryption_in_file = int(input())

            # if user wants to provide own encryption
            if encryption_in_file == 1:
                encryption_key = input("Enter your encryption key: ")

            # if user wants to read from file
            elif encryption_in_file == 2:
                file = str(input("Provide the file where your key is located including the extension: "))
                encryption_key = read_encryption_key(file)
            else:
                SystemExit("No valid choice provided")

            print("Encoding...")

            # def Encode(encryption_key, src, message, dest):
            Encode(encryption_key, src, encrypted_message, dest)

    elif func == '2':
        layers = int(input("How many layers of encryption 1 or 2? "))
        if layers == 1:
            print("Enter Source Image Path")
            src = input()

            # getting location of key from user
            print("Where is the encryption key? ")
            print("1. I will type it.")
            print("2. It's in a file")
            key_location = int(input())

            # getting key from file/user
            if key_location == 1:
                encryption_key = input("Type your encryption key: ")
            elif key_location == 2:
                file_location = input("Enter the path of the file: ")
                encryption_key = read_encryption_key(file_location)
            print("Decoding...")
            decoded_message = Decode(src, encryption_key, 1)
            print("Decoded message is: {}".format(decoded_message))

        elif layers == 2:
            print("Enter Source Image Path")
            src = input()
            print("Enter rsa private key file path:")
            private_key_path = input()
            print("Where is the encryption key? ")
            print("1. I will type it.")
            print("2. It's in a file")
            key_location = int(input())

            # getting key from file/user
            if key_location == 1:
                encryption_key = input("Type your encryption key: ")
            elif key_location == 2:
                file_location = input("Enter the path of the file: ")
                encryption_key = read_encryption_key(file_location)
            print("Decoding lsb...")
            decoded_message = Decode(src, encryption_key, 2)

            print("decoding rsa encryption...")
            rsa_decoded_msg = rsa_decrypt(private_key_path, decoded_message)
            #def rsa_decrypt(private_key_file, encrypted_message):

            print("Decoded message is: {}".format(rsa_decoded_msg))
    else:
        print("ERROR: Invalid option chosen")

Stego()

