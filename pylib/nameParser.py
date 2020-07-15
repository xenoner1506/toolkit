import os

def nameParse(filepath, pardelimiter='--', tagdelimiter='-'):
    dirname = os.path.dirname(filepath)
    basename = os.path.basename(filepath)
    name, ext = basename.split('.')
    parameters = name.split(pardelimiter)
    if ext != "hdf5":
        raise Exception("Not .hdf5 data")
    if parameters[0] != "CLs":
        raise Exception("Not CLs data")
    fileDict = dict()
    fileDict["mode"] = parameters[1]
    for parameter in parameters[2:]:
        tags = parameter.split(tagdelimiter)
        fileDict[tags[0]] = tags[1:]
    return fileDict
