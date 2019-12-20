import json

data = open("a2oj_copy.txt")
data = data.read()
y = json.loads(data)
# print(len(y))
for a in y:
    print(a['ladder name'])