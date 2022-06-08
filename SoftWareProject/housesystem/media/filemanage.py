import os

path = './'
for file in os.listdir(path):
    suffix = file.split('.')
    if len(suffix) == 1:
        os.renames(file, file + '.png')

