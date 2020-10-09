from encryptor import Encryptor


def encrypt_file(path, public_key, key_length):
    with open(path, 'rb') as file:
        file_bytes = file.read()
        file_bytes = Encryptor(key_length, public_key).encrypt(file_bytes)

        file.close()

        file = open(path, 'wb')
        file.write(file_bytes)
