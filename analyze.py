import mli_lib as mli
import operator
import ast

occurrence = {}

def add_dict(words,add):
    for word in words:
        count = occurrence.get(word, -1)
        if count == -1:
            occurrence[word] = 1
        else:
            occurrence[word] += add

dataFile = open("data.txt","r")
line = dataFile.readline()
new_list = ast.literal_eval(line)

for part in new_list:
    words = str(part[0]).split(" ")
    count = part[1]
    add_dict(words,count)

sorted_x = sorted(occurrence.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_x)
