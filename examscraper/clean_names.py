import os, re
digits = "".join([str(i) for i in range(10)])

directory = "M:/OneDrive - NTNU/Subjects/17 Statistikk/Exams/"
for filename in os.listdir(directory):
    print(filename)
    splitname = re.split("(eks|[0-9]+)", filename)
    splitname = list(filter(lambda x: x != '', splitname))
    print(splitname)
    splitname[1], splitname[2] = splitname[2], splitname[1]
    splitname.insert(3, "-")
    newname = "".join(splitname)
    print("{} to {}".format(filename, newname))
    os.rename(directory+filename,directory+newname)
