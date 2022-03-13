import json


def read(file):
    file_to_read = open(file, 'r', encoding='utf8')
    var = eval(file_to_read.read())
    file_to_read.close()
    return var


def write_txt(file, var):
    file_to_write = open(file, 'w', encoding='utf8')
    data = str(var)
    file_to_write.write(data)
    file_to_write.close()


def write_json(file, var):
    file_to_write = open(file, 'w', encoding='utf8')
    json.dump(var, file_to_write, ensure_ascii=False)
    file_to_write.close()
