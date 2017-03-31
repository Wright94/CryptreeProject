import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend


def generateKey(salt, backend, info):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=info,
        backend=backend
    )
    key = hkdf.derive(b"input key")
    # print(key)
    return key


def validateKey(salt, backend, info, key):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=info,
        backend=backend
    )
    hkdf.verify(b"input key", key)


def mainKeyGen():

    salt = os.urandom(16)
    backend = default_backend()
    info = b"hkdf-example"
    key = generateKey(salt, backend, info)
    return key

if __name__ == '__main__':
    mainKeyGen()
