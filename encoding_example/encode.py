import stego


def main():
    # loading key phrase
    key_phrase_file = "key_phrase.txt"
    key_phrase = stego.read_key_phrase(key_phrase_file)

    # Generating keys
    public_key, private_key = stego.generate_rsa_key(512)

    # Saving public key to file for demonstration purposes
    public_key_file = "public_key_test0.pem"
    stego.save_public_key(public_key_file, public_key)

    # Saving private key to file for demonstration purposes
    private_key_file = "private_key_test0.pem"
    stego.save_private_key(private_key_file, private_key)

    # Encrypting key phrase with rsa encryption
    encrypted_key_phrase = stego.rsa_encrypt(key_phrase, public_key)

    # Saving encrypted key phrase to file
    encrypted_key_phrase_file = "encrypted_key_phrase.txt"
    stego.save_encrypted_key_phrase(encrypted_key_phrase_file, encrypted_key_phrase)

    # Encoding text onto the image
    message = "This is my hidden text in an image"
    base_image = "surfer_in_barrel.png"
    image_with_encoded_txt = "image_with_encoded_text.png"

    stego.encode(key_phrase, base_image, message, image_with_encoded_txt)


main()
