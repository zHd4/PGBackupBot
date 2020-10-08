from encryptor import Encryptor


def encrypt_file(path, public_key, key_length):
    with open(path, 'wb') as file:
        file_bytes = file.read()
        file_bytes = Encryptor(key_length, public_key).encrypt(file_bytes)

        file.write(file_bytes)
