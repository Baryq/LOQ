from FrequentFunctions import read, write_json

path1 = 'convertionFolder/dct.txt'
path2 = 'convertionFolder/dct.json'

write_json(path2, read(path1))
