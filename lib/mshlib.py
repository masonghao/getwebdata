# 获取本地文件的内容到字符串
def getFileContent(fileName, mods = 'rb'):
    file = open(fileName, mods)
    fileCode = file.read()
    file.close()
    return fileCode

# 输出字符串到一个本地文件
def putFileContent(fileName, filecode, mods = 'wb'):
    f = open(fileName, mods)
    lens = f.write(filecode)
    f.close()
    return lens
