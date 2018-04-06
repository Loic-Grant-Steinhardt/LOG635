### ALGORITHME KNN ###
import csv
import random
import math
import operator
<<<<<<< HEAD
import json
from tkinter import filedialog
from tkinter import *
import ctypes
from ctypes.wintypes import HWND, LPWSTR, UINT

import pickle

from multiprocessing import Pool
pool = Pool()

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

IDYES = 6
IDNO = 7

choix = Mbox('Algo KNN', 'Voulez-vous importer un seul fichier ?', 4)

if choix==IDNO:
  # Lire les fichiers
  root = Tk()
  root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Sélectionner les données",filetypes = (("Données","*.csv"),("jpeg files","*.jpg")))
  file_txt = open(root.filename, "r", -1, "utf-8").read()
  set(w.lower() for w in file_txt)
  lines = file_txt.split("\n")
  headers = lines[0].split(',')

  root = Tk()
  root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Sélectionner les données",filetypes = (("Données","*.csv"),("jpeg files","*.jpg")))
  file_txt = open(root.filename, "r", -1, "utf-8").read()
  set(w.lower() for w in file_txt)
  lines2 = file_txt.split("\n")
  
elif choix==IDYES:
  root = Tk()
  root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Sélectionner les données",filetypes = (("Données","*.csv"),("jpeg files","*.jpg")))
  file_txt = open(root.filename, "r", -1, "utf-8").read()
  set(w.lower() for w in file_txt)
  lines = file_txt.split("\n")
  headers = lines[0].split(',')
=======

# Lire les fichiers
file_txt = open("Dataset.csv", "r", -1, "utf-8").read()
set(w.lower() for w in file_txt)
lines = file_txt.split("\n")
headers = lines[0].split(',')

file_txt = open("Evaluations.csv", "r", -1, "utf-8").read()
set(w.lower() for w in file_txt)
lines2 = file_txt.split("\n")
>>>>>>> aeada7d6cb39a1ca52f3d7aec92b9b2ca4950eec
          
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
    "18-24": 1,
    "25-34": 2,
    "35-44": 3,
    "45-54": 4,
    "55-64": 5,
    "65+": 6
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
  "Doctorat" : 1,
  "Matrise" : 2,
  "Université" : 3,
  "Collège ou université aucun certificat ou diplome" : 4,
  "Certificat ou diplome professionel" : 5,
  "À quitté l'école à 18 ans" : 6,
  "À quitté l'école à 17 ans" : 7,
  "À quitté l'école à 16 ans" : 8,
  "À quitté l'école avant 16 ans" : 9
}
ethniciteMultiplier = {
    "Blanc": 1,
    "Mixed-Blanc/Asiatique": 2,
    "Mixed-Blanc/Noir": 3,
    "Asiatique": 4,
    "Noir": 5,
    "Autre": 6
}

# Détermine si une valeur est numérique
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

# Calcule de la distance Euclédienne entre deux éléments
def calculerDistance(first, second, length):
  dist = 0
  exp = 2

  # Parcours des attributs et incrémentation
  for x in range(length):
    dist = dist + pow((first[x] - second[x]), exp)
    
  return math.sqrt(dist)

# Déterminer les k plus proches voisins de chaque éléments d'un dataset
def plusProchesVoisins(dataset, evalSet, k):
  voisins = []
  distances = []
  length = len(evalSet) - 1

  # Parcourir le dataset
  for x in range(len(dataset)):
    dist = calculerDistance(evalSet, dataset[x], length)
    distances.append((dataset[x], dist))

  # Trier les valeurs
  distances.sort(key = operator.itemgetter(1))

  # Retourner les voisins en ordre du plus proche
  for x in range(k):
    voisins.append(distances[x][0])
    
  return voisins

# Retourner la préciction de Nicotine basé sur les plus proches voisins
def getPrediction(voisins):
  attributs = {}

  # Parcourir chaque attribut
  for i in range(len(voisins)):
    attribut = voisins[i][-1]

    # Si l'attribut courant se trouve dans la liste d'attributs
    if attribut in attributs:
      attributs[attribut] = attributs[attribut] + 1
    else:
      attributs[attribut] = 1

  # Trier les attributs    
  attributsTrie = sorted(attributs.items(), key = operator.itemgetter(1), reverse = True)

  # Retourner le premier élément dans la liste triée
  return attributsTrie[0][0]

# Evaluation de la precision des predictions
def evalPrecision(evalSet, predictions):
  pareil = 0

  # Parcourir evalSet
  for x in range(len(evalSet)):
    # Si la valeur du dernier attribut est égale à la valeur prédite
    if evalSet[x][-1] == predictions[x]:
      pareil += 1

  pourcentage = (pareil / float(len(evalSet))) * 100.0
  return pourcentage

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

      # Mettre Nicotine à la fin
      if(isTraining):
        nicotineValue = row[indexNicotine]
        row.pop(indexNicotine)
        row.insert(len(row), nicotineValue)
      
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
        # Ajouter les données au dataset
        datas.insert(len(datas), row)

  # Retourner le dataset
  return datas

choix2 = Mbox('Algo KNN', 'Voulez-vous importer des données entrainées ?', 4)
if choix2==IDYES:
    dataset = pickle.load( open( "sauvegarde.p", "rb" ) )
    evalSet = createDataset(lines2, False)
    evalSet = ajustValues(evalSet)

# Training set
<<<<<<< HEAD
if choix2==IDNO:
    dataset = createDataset(lines, True)
    if choix == IDYES :
      evalSet = dataset[int(len(dataset)/2):]
      dataset = dataset[:int((len(dataset))/2)]
    elif choix == IDNO :
      evalSet = createDataset(lines2, False)

    dataset = ajustValues(dataset)
    evalSet = ajustValues(evalSet)

choix2 = Mbox('Algo KNN', 'Voulez-vous sauvegarder les données entrainées ?', 4)
if choix==IDYES:
    with open('sauvegarde.p', 'wb') as f:
        pickle.dump(dataset, f)
    
=======
dataset = createDataset(lines, True)
dataset = ajustValues(dataset)

# Evaluation set
evalSet = createDataset(lines2, False)
evalSet = ajustValues(evalSet)

# AFfichage
>>>>>>> aeada7d6cb39a1ca52f3d7aec92b9b2ca4950eec
print("Training set length   : " + str(len(dataset)) + " entries")
print("Evaluation set length : " + str(len(evalSet)) + " entries")
print("")

print("Prédictions")
print("*************************************")
print("")

k = 2
predictions = []

# Parcourir evalSet
for x in range(len(evalSet)):
  voisins = plusProchesVoisins(dataset, evalSet[x], k)
  prediction = getPrediction(voisins)
  predictions.insert(len(predictions), prediction)
  
  print(' Prédiction = ' + repr(prediction) + ', Valeur = ' + repr(evalSet[x][-1]))
  
accuracy = evalPrecision(evalSet, predictions)
print("-------------------------------------")
print(' ACCURACY  = ' + repr(accuracy) + '%')
