### ALGORITHME KNN ###
import csv
import random
import math
import operator

# Lire les fichiers
file_txt = open("Dataset.csv", "r", -1, "utf-8").read()
set(w.lower() for w in file_txt)
lines = file_txt.split("\n")
headers = lines[0].split(',')

file_txt = open("Evaluations.csv", "r", -1, "utf-8").read()
set(w.lower() for w in file_txt)
lines2 = file_txt.split("\n")
headers2 = lines2[0].split(',')
          
# Élimination de certaines valeurs
indexId = headers.index("Id")
del headers[indexId]

indexNicotine = headers.index("Nicotine")
del headers[indexNicotine]
headers.insert(len(headers), "Nicotine")

# Initialisation de variables
dataset = []
evalSet = []
minMax = {}

# Initialisation des min/max
for value in headers:
  temp = {'min': None,'max': None}
  minMax['' + value] = temp

# Multipliers
ageMultiplier = {
    "18-24": 0.17,
    "25-34": 0.34,
    "35-44": 0.51,
    "45-54": 0.68,
    "55-64": 0.85,
    "65+": 1.00
}
genreMultiplier = {
    "Male": 1,
    "Female": 0,
}
paysMultiplier = {
    "UK": 1,
    "USA": 2,
    "Canada": 3,
    "Australie": 4,
    "Autre": 5,
    "Nouvelle Zelande": 6,
    "Republique d'Ireland": 7,    
}
educationMultiplier = {
  "Doctorat" : 0.11,
  "Matrise" : 0.22,
  "Université" : 0.33,
  "Collège ou université aucun certificat ou diplome" : 0.44,
  "Certificat ou diplome professionel" : 0.55,
  "À quitté l'école à 18 ans" : 0.66,
  "À quitté l'école à 17 ans" : 0.77,
  "À quitté l'école à 16 ans" : 0.88,
  "À quitté l'école avant 16 ans" : 1
}
ethniciteMultiplier = {
    "Blanc": 0.17,
    "Mixed-Blanc/Asiatique": 0.34,
    "Mixed-Blanc/Noir": 0.51,
    "Asiatique": 0.68,
    "Noir": 0.85,
    "Autre": 1.00
}

# Détermine si une valeur est numérique
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def euclideanDistance(instance1, instance2, length):
  distance = 0
  for x in range(length):
    distance += pow((instance1[x] - instance2[x]), 2)
  return math.sqrt(distance)

def getNeighbors(dataset, testInstance, k):
  distances = []
  length = len(testInstance)-1
  for x in range(len(dataset)):
    dist = euclideanDistance(testInstance, dataset[x], length)
    distances.append((dataset[x], dist))
  distances.sort(key=operator.itemgetter(1))
  neighbors = []
  for x in range(k):
    neighbors.append(distances[x][0])
  return neighbors

def getResponse(neighbors):
  classVotes = {}
  for x in range(len(neighbors)):
    response = neighbors[x][-1]
    if response in classVotes:
      classVotes[response] += 1
    else:
      classVotes[response] = 1
  sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
  return sortedVotes[0][0]

def getAccuracy(evalSet, predictions):
  correct = 0
  for x in range(len(evalSet)):
    if evalSet[x][-1] == predictions[x]:
      correct += 1
  return (correct/float(len(evalSet))) * 100.0

# Ajuster les valeurs entre 0 et 1 selon la méthode avec l'étendu
def ajustValues(datas):
  for i, data in enumerate(datas):
    for j, value in enumerate(data):
      header = headers[j]
      minValue = minMax[''+header]['min']
      maxValue = minMax[''+header]['max']

      # S'il y a des valeurs présentes
      if(minValue is not None and maxValue is not None):
        etendu = maxValue - minValue
        currentValue = data[j]

        # Ajuster la valeur si l'étendu est supérieur à 0
        if(etendu == 0):
          newValue = 0
        else:
          newValue = (currentValue - minValue) / etendu
          newValue = round(newValue,4)

        # Remplacer la valeur dans le dataset
        datas[i][j] = newValue
  return datas

def createDataset(lines, isTraining):
  datas = []
  # Loop sur chaque ligne du fichier
  for index, line in enumerate(lines):
    row = line.split(',')

    # Élimination de certaines valeurs
    del row[indexId]

    # On skip la première ligne (headers)
    if index > 0 :
      del row[-1]
      valeurAberrante = False

      # Conserver la valeur de la Nicotine
      nicotineValue = float(row[indexNicotine])
      
      # Loop sur chaque valeur d'une ligne
      for col, value in enumerate(row):
        header = "" + headers[col]
        value = value.strip()

        # Enlever les pourcentages (%)
        if value.find("%") != -1 :
          value = value.replace("%", "")
          row[col] = value

        # Élimination des valeurs aberrantes
        # Age impossible
        if(header == "Age"):
          if(value not in ageMultiplier):
            valeurAberrante = True
            break
          else:
            value = ageMultiplier[value]
            row[col] = value

        # Education impossible 
        if(header == "Education"):
          if(value not in educationMultiplier):
            valeurAberrante = True
            break
          else:
            value = educationMultiplier[value]
            row[col] = value

        # Genre impossible
        if(header == "Genre"):
          if(value not in genreMultiplier):
            valeurAberrante = True
            break
          else:
            value = genreMultiplier[value]
            row[col] = value

        # Ethnicité impossible
        if(header == "Ethnicité"):
          if(value not in ethniciteMultiplier):
            valeurAberrante = True
            break
          else:
            value = ethniciteMultiplier[value]
            row[col] = value

        # Pays impossible
        if(header == "Pays"):
          if(value not in paysMultiplier):
            valeurAberrante = True
            break
          else:
            value = paysMultiplier[value]
            row[col] = value

        # Retirer 'Nicotine' de la row
        if(col == indexNicotine):
          value = float(value)

          '''# Un peu sketch mais ca va pour l'instant
          currentMin = minMax['Nicotine']['min']
          currentMax = minMax['Nicotine']['max']

          if(currentMin is None):
            minMax['Nicotine']['min'] = float(value)
          elif(float(value) < currentMin):
            minMax['Nicotine']['min'] = float(value)

          if(currentMax is None):
            minMax['Nicotine']['max'] = float(value)
          elif(float(value) > currentMax):
            minMax['Nicotine']['max'] = float(value)'''
          
          row.pop(col)
          #break

        # Si la valeur est numerique
        if(isfloat(value)):
          # Convertir string en float
          value = float(value)
          row[col] = value

          # Affecter le tableau minMax si nécessaire
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

      # Ajouter la valeur si elle n'est pas aberrante
      if not valeurAberrante:
        # Mettre 'Nicotine' à la fin
        row.insert(len(row), nicotineValue)

        # Ajouter les données au dataset
        datas.insert(len(datas) - 1, row)

  # Retourner le dataset
  return datas


# Training set
dataset = createDataset(lines, True)
#dataset = ajustValues(dataset)

# Evaluation set
evalSet = createDataset(lines2, False)
#evalSet = ajustValues(evalSet)

'''print("Training set length   : " + str(len(dataset)) + " entries")
print("Evaluation set length : " + str(len(evalSet)) + " entries")'''

predictions=[]
k = 3

for x in range(len(evalSet)):
  neighbors = getNeighbors(dataset, evalSet[x], k)
  result = getResponse(neighbors)
  predictions.append(result)
  print('> predicted=' + repr(result) + ', actual=' + repr(evalSet[x][-1]))
  
accuracy = getAccuracy(evalSet, predictions)
print('Accuracy: ' + repr(accuracy) + '%')
