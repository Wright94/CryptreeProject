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


def Test2(rootDir, nodeId):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        files.append([nodeId, lists])
        print(path)
        nodeId += 1
        if os.path.isdir(path):
            Test2(path, nodeId)
            nodeId = len(files)


rootDir = "ThisDirectory"
files = []
nodeId = 0
Test2(rootDir, nodeId)
print(files)
