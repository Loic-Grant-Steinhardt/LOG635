import json

file_txt = open("Dataset.csv",'r').read()
set(w.lower() for w in file_txt)

#print(file_txt)

headers = []
datas = []

for index, line in enumerate(file_txt.split("\n")):
    data = {}
    split = line.split(',')
    
    if index == 0 :
        headers = split
    else:
        del split[-1]
        if (len(headers) > 0):
            for col, value in enumerate(split):
                data["" + headers[col]] = value.strip()
            datas.insert(len(datas) - 1, data);


print(str(len(datas)) + " entrées")

# Exemple accéder à une entrée : datas[index]['Pays']
