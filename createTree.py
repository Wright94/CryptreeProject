# =======================================
# This method can simply iterate through a filesystem, noting each folder or file.
# =======================================

# import os
# def Test2(rootDir):
#     print("Ooooooo " + rootDir)
#     for lists in os.listdir(rootDir):
#         print("Oi oi " + lists)
#         path = os.path.join(rootDir, lists)
#         print(path)
#         if os.path.isdir(path):
#             Test2(path)


# Test2("ThisDirectory")


# =======================================
# Used for storing this tree information,
# More Specifically, this method creates a unique id for each node of the tree.
# The Tree can now be referenced by a specific node.
# =======================================

import os

import sys

from keyGeneration import mainKeyGen
from encryptDecryptStr import encrypt, decrypt


def Test2(rootDir, nodeId, files):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        parNode = getParentNodePath(path, files)
        files.append([nodeId, path, lists, parNode])
        print(path)
        nodeId += 1
        # print(nodeId)
        if os.path.isdir(path):
            Test2(path, nodeId, files)
            # print(len(files))
            nodeId = len(files)
            # print(nodeId)


def getParentNodePath(path, files):
    for i in range(0, len(files)):
        if files[i][1] == os.path.dirname(path):
            parNode = files[i][0]
            return parNode


def getParentNode(node, files):
    for i in range(0, len(files)):
        if files[i][0] == node:
            parNode = files[i][3]
            return parNode


def getSksNode(node, tempSks):
    for i in range(0, len(tempSks)):
        if tempSks[i][0] == node:
            return i


def getFksNode(node, tempFks):
    for i in range(0, len(tempFks)):
        if tempFks[i][0] == node:
            return i


def generateKeys(tempNodeKeys, files, tempSks, tempBks, tempFks):
    for i in range(0, len(files)):

        if i == 0 or (os.path.isdir(str(files[i][1]))):
            # Sk
            tempNodeKeys.append(["Sk:", mainKeyGen()])
            # Bk
            tempNodeKeys.append(["Bk:", mainKeyGen()])
            # Fk
            tempNodeKeys.append(["Fk:", mainKeyGen()])
            # Dk
            tempNodeKeys.append(["Dk:", mainKeyGen()])
            # Call function to generate crypto links
            generateSkpfToSkfLink(tempNodeKeys, i, tempSks, files)
            generateSkfToBkfLink(tempNodeKeys, i, files)
            generateBkfToDkfLink(tempNodeKeys, i, files)
            generateSkfToFkfLink(tempNodeKeys, i, files, tempFks)
            generateBkfToBkpfLink(tempNodeKeys, i, files, tempBks, tempSks)

        if (os.path.isfile(str(files[i][1]))):
            tempNodeKeys.append(["Dkf:", mainKeyGen()])
            # =========Was to be used for encrypting files===========
            # file_name = files[i][1]
            # dkKey = tempNodeKeys[0][1]
            # iv, ciphertext, tag = encrypt_file(file_name, dkKey)
            # decrypt_file(dkKey, iv, file_name, tag)
            generateFkfToDkfLink(tempNodeKeys, i, tempFks, files)

            tempNodeKeys[:] = []


def generateSkpfToSkfLink(tempKeys, listPos, tempSks, files):
    # tempSks[] must be global!!!, will be 2d again, each sk stored with its node id.
    tempSks.append([listPos, (tempKeys[0][1])])
    # Skp(f) --> Sk(f). Except for root since it has no parent
    if listPos != 0:
        parNode = getParentNode(listPos, files)
        tempSksnode = getSksNode(parNode, tempSks)
        iv, cryptoLink, tag = encrypt(tempSks[tempSksnode][1], tempKeys[0][1], b'Additional Data, used for Authentication')
        files[listPos].append(cryptoLink)
    else:
        files[listPos].append("Root of Tree")


def generateSkfToBkfLink(tempKeys, listPos, files):
    iv, cryptoLink, tag = encrypt(tempKeys[0][1], tempKeys[1][1], b'Additional Data, used for Authentication')
    files[listPos].append(cryptoLink)


def generateBkfToDkfLink(tempKeys, listPos, files):
    iv, cryptoLink, tag = encrypt(tempKeys[1][1], tempKeys[3][1], b'Additional Data, used for Authentication')
    files[listPos].append(cryptoLink)


def generateSkfToFkfLink(tempKeys, listPos, files, tempFks):
    tempFks.append([listPos, (tempKeys[2][1])])
    iv, cryptoLink, tag = encrypt(tempKeys[0][1], tempKeys[2][1], b'Additional Data, used for Authentication')
    files[listPos].append(cryptoLink)


def generateBkfToBkpfLink(tempKeys, listPos, files, tempBks, tempSks):
    # tempBks[] must be global!!!, will be 2d again, each bk stored with its node id.
    tempBks.append([listPos, (tempKeys[1][1])])
    # Bk(f) --> Bkp(f). Except for leaf folders since it has no descendant.
    if listPos != 0:
        parNode = getParentNode(listPos, files)
        tempBksnode = getSksNode(parNode, tempSks)
        iv, cryptoLink, tag = encrypt(tempKeys[1][1], tempSks[tempBksnode][1], b'Additional Data, used for Authentication')
        files[listPos].append(cryptoLink)
    else:
        files[listPos].append("Root of Tree")


def generateFkfToDkfLink(tempKeys, listPos, tempFks, files):
    parNode = getParentNode(listPos, files)
    tempFksNode = getFksNode(parNode, tempFks)
    iv, cryptoLink, tag = encrypt(tempFks[tempFksNode][1], tempKeys[0][1], b'Additional Data, used for Authentication')
    files[listPos].append(cryptoLink)


# ===================================================================================
# Unfortunately I was unable to successfully encrypt and decrypt each file using Dkf
# There was a bug within the code which I could not find.
# ===================================================================================

# def encrypt_file(file_name, key):
#     with open(file_name, 'rb') as fo:
#         plaintext = fo.read()
#     iv, enc, enctag = encrypt(key, plaintext, b'Additional Data, used for Authentication')
#     with open(file_name + ".enc", 'wb') as fo:
#         fo.write(enc)
#     print("\n")
#     print(enctag)
#     print("\n")
#     return iv, enc, enctag
#
#
# def decrypt_file(dkKey, iv, file_name, dectag):
#     with open(file_name, 'rb') as fo:
#         ciphertext = fo.read()
#     print("\n")
#     print(dectag)
#     print("\n")
#     dec = decrypt(dkKey, b'Additional Data, used for Authentication', iv, ciphertext, dectag)
#     print(dec)
#     with open(file_name[:-4], 'wb') as fo:
#         fo.write(dec)


def mainTreeBuild(root):

    rootDir = root
    # Below is the format used to store the tree,
    # files = [index, path, nodeName, parentID, Skp(f)-->Skf, Sk-->Bk, Bk-->Dk, Sk-->Fk, Bkf-->Bkp(f)]
    files = [[0, rootDir, rootDir, 0]]
    print("Visualisation of Cryptree starting from root node " + rootDir + ":")
    print("===================================================================")
    Test2(rootDir, 1, files)
    print("\n")
    print(
        "Below is the output of constructing the tree structure. See how it only contains location and reference information:")
    print(
        "====================================================================================================================")
    print(files)
    print("\n")
    tempNodeKeys = []
    # tempSks is a 2d array with each folders Sk with the associated node ID.
    tempSks = []
    tempBks = []
    tempFks = []
    generateKeys(tempNodeKeys, files, tempSks, tempBks, tempFks)
    print("\n")
    print("Here is the Cryptree once all Cryptographic links have been implemented:")
    print("========================================================================")
    print(files)

if __name__ == '__main__':
    mainTreeBuild(sys.argv[1])
