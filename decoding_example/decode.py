import Stego


def main():
    # load encrypted key phrase
    encrypted_phrase_file = "encrypted_key_phrase.txt"
    encrypted_key_phrase = Stego.read_encrypted_key_phrase(encrypted_phrase_file)

    # load private key
    my_private_key = Stego.load_private_key("private_key_test0.pem")

    # decrypt key phrase with private key
    key_phrase = Stego.decrypt_with_private_key(my_private_key, encrypted_key_phrase)

    # decode text from image
    img_src = "image_with_encoded_text.png"
    decoded_text = Stego.decode(img_src, key_phrase)
    print(f'decoded text is: {decoded_text}')

main()
