import numpy as np
from matplotlib import pyplot as plt

data_name= "Cs137.Spe"
#diamo una struttura dati al nostro file di acquisizione
righe_str = []
data = []

#NOTA il file aveva un carattere speciale orrendo --> errors= replace crea una istanza e  risolve il problema
#apro i dati con open()
with open(data_name, 'r' , encoding='utf-8', errors= 'replace') as file: 

    for line in file:
        righe = line.strip()

        try:
            numero = int(righe)
            data.append(numero)
        except ValueError:
            #righe_str.append(numero)
            continue

data = data[: -5]
print(f'La shape del tensore dei dati è {np.shape(data)}, il numero dei canali è {np.shape(data)[0]}') #occhio alle tuple!
#print('stringhe', righe_str)

#creiamo l'istogramma
bins = np.shape(data)[0]
#plt.hist(data, bins, edgecolor='blue', facecolor='none')

x = np.linspace(0, bins, bins)
plt.plot(x ,data, color='green')
plt.show()



