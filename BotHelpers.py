import os

def Mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def FileExists(path):
    return os.path.exists(path)

def Rm(path):
    if os.path.exists(path):
        os.remove(path)
        return not os.path.exists(path)
    return False

def PreparePath(path):
    return path.replace("..", "")
