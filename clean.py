#!/usr/bin/env python
# -*- coding: utf-8 -*

import json
from tkinter import filedialog
from tkinter import *


'''root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Sélectionner les données",filetypes = (("Données","*.csv"),("jpeg files","*.jpg")))
root.destroy()'''

file_txt = open("Dataset.csv", "r", -1, "utf-8").read()
set(w.lower() for w in file_txt)

headers = []
datas = []
minMax = {}


ageMultiplier = {
    "18-24": 0.17,
    "25-34": 0.34,
    "35-44": 0.51,
    "45-54": 0.68,
    "55-64": 0.85,
    "65+": 1.00
}

lines = file_txt.split("\n")
headers = lines[0].split(',')

# Élimination de certaines valeurs
indexId = headers.index("Id")
del headers[indexId]

IndexEthni = headers.index("Ethnicité")
del headers[IndexEthni]

for value in headers:
  temp = {'min': None,'max': None}
  minMax['' + value] = temp

# Détermine si une valeur est numérique
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

for index, line in enumerate(lines):
    data = {}
    split = line.split(',')

    # Élimination de certaines valeurs
    del split[indexId]
    del split[IndexEthni]
    
    if index > 0 :
        del split[-1]
        if (len(headers) > 0):
            for col, value in enumerate(split):
                valeurAberrante = False
                header = "" + headers[col]
                value = value.strip()

                # Élimination des valeurs aberrantes
                # Age impossible
                if(header == "Age"):
                  if(value not in ageMultiplier):
                    valeurAberrante = True
                    break
                
                # Enlever les pourcentages (%)
                if value.find("%") != -1 :
                    value = value.replace("%", "")

                # si la valeur est numerique
                if(isfloat(value)):
                  currentMin = minMax[header]['min']
                  currentMax = minMax[header]['max']

                  if(currentMin is None):
                    minMax[header]['min'] = float(value)
                  elif(float(value) < currentMin):
                    minMax[header]['min'] = float(value)

                  if(currentMax is None):
                    minMax[header]['max'] = float(value)
                  elif(float(value) > currentMax):
                    minMax[header]['max'] = float(value)
            
                data[header] = value
            if not valeurAberrante :
                datas.insert(len(datas) - 1, data);


'''
Ajuster les valeurs entre 0 et 1
Selon la méthode avec l'étendu
'''
for i, data in enumerate(datas):
  #print(data)
  for j, header in enumerate(data):
    minValue = minMax[''+header]['min']
    maxValue = minMax[''+header]['max']

    if(minValue is not None and maxValue is not None):
      etendu = maxValue - minValue
      currentValue = float(data[header])
      newValue = (currentValue - minValue) / etendu
      datas[i][header] = newValue

# Affichage console
print(str(len(datas)) + " entrées")
