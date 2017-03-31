import os

from cryptography.hazmat.backends import default_backend
from keyGeneration import mainKeyGen
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)


def encrypt(key, plaintext, associated_data):
    # Generate a random 96-bit IV.
    iv = os.urandom(12)

    # Construction of an AES-GCM Cipher. Key generated using keyGeneration HKDF function.
    # Iv has been pseudo randomly generated.
    encryptor = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend()).encryptor()

    # associated_data will be authenticated but not encrypted,
    # it must also be passed in on decryption.
    encryptor.authenticate_additional_data(associated_data)

    # Encrypt the plaintext and get the associated ciphertext.
    # GCM does not require padding.
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    # print("This is the ciphertext, result of encrypting using key from keyGen: " + str(ciphertext))
    return iv, ciphertext, encryptor.tag


def decrypt(key, associated_data, iv, ciphertext, tag):
    # Construct a Cipher object, with the key, iv, and additionally the
    # GCM tag used for authenticating the message.
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()

    # We put associated_data back in or the tag will fail to verify
    # when we finalize the decryptor.
    decryptor.authenticate_additional_data(associated_data)

    # Decryption gets us the authenticated plaintext.
    # If the tag does not match an InvalidTag exception will be raised.
    return decryptor.update(ciphertext) + decryptor.finalize()


# key = mainKeyGen()
# # print("Check to see what key has been returned by keyGen function: " + str(key))
# iv, ciphertext, tag = encrypt(key, b"Holy smokes, it works!! Im not sure what is going on, please go all non ascii on me", b"authenticated but not encrypted payload")
#
# print(decrypt(key, b"authenticated but not encrypted payload", iv, ciphertext, tag))

# ===========================================================================================================

