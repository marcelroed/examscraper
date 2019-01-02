import os, re

rules = [
    lambda s: re.sub(r"(Aug)", "S", s),
    lambda s: re.sub(r"(Jun|Mai)", "V", s),
    lambda s: re.sub(r"(Nov|Des)", "H", s)
]

directory = "M:/OneDrive - NTNU/Subjects/17 Statistikk/Exams/"

renames = []

for filename in os.listdir(directory):
    newname = filename
    for rule in rules:
        newname = rule(newname)
    renames.append((filename, newname))

renames.sort()

# Confirm renaming
print('\n'.join(['{} -> {}'.format(*rename) for rename in renames]))
inp = input('Are you sure you want to commit these changes? (y/n)')
if inp.lower() == 'y':
    for filename, newname in renames:
        os.rename(directory+filename,directory+newname)
