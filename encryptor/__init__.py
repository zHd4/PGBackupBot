from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class Encryptor:
    def __init__(self, key_length, public_key):
        self.__length = int(key_length / 16)
        self.__crypto = PKCS1_OAEP.new(RSA.importKey(public_key))

    def encrypt(self, data_bytes):
        encrypted_chunks = []

        for block in self.__split_to_blocks(data_bytes):
            encrypted_chunks.append(self.__crypto.encrypt(block))

        return self.__join_blocks(encrypted_chunks)

    def __split_to_blocks(self, data):
        size, length = len(data), self.__length
        return [data[i:i + length] for i in range(0, size, length)]

    # noinspection PyMethodMayBeStatic
    def __join_blocks(self, blocks):
        return b''.join(blocks) if len(blocks) > 0 else blocks
