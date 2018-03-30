### ALGORITHME KNN ###

# Lire les fichiers
file_txt = open("Dataset.csv", "r", -1, "utf-8").read()
set(w.lower() for w in file_txt)
lines = file_txt.split("\n")
headers = lines[0].split(',')

file_txt = open("Evaluations.csv", "r", -1, "utf-8").read()
set(w.lower() for w in file_txt)
lines2 = file_txt.split("\n")

# Élimination de certaines valeurs
indexId = headers.index("Id")
del headers[indexId]

IndexEthni = headers.index("Ethnicité")
del headers[IndexEthni]

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

# Détermine si une valeur est numérique
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

# Ajuster les valeurs entre 0 et 1 selon la méthode avec l'étendu
def ajustValues(datas):
  for i, data in enumerate(datas):
    for j, value in enumerate(data):
      #print(value)
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

def createDataset(lines):
  datas = []
  # Loop sur chaque ligne du fichier
  for index, line in enumerate(lines):
    row = line.split(',')

    # Élimination de certaines valeurs
    del row[indexId]
    del row[IndexEthni]

    # On skip la première ligne
    if index > 0 :
      del row[-1]
      valeurAberrante = False
      
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
      if not valeurAberrante :
        datas.insert(len(datas) - 1, row)

  return datas


# Training set
dataset = createDataset(lines)
dataset = ajustValues(dataset)

# Evaluation set
evalSet = createDataset(lines2)
evalSet = ajustValues(evalSet)

print("Training set length   : " + str(len(dataset)) + " entries")
print("Evaluation set length : " + str(len(evalSet)) + " entries")
