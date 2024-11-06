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
 
print("--------")
#eliminiamo il segnale di backgrouncontinuum dai dati

a = 774  #conteggi canale A
b = 979 #conteggi canale B
N_ch = b - a #conteggi fra A e B

ch_a = data[a]
ch_b = data[b]

def continum(ch_a, ch_b):
    return (ch_a + ch_b)*N_ch/2

span = data[a : b]
def AreaPicco(data):
    return sum(span) - continum(ch_a, ch_b)

print(f"Questa è la stima dell'area del continum {continum(ch_a, ch_b)} \nQuesta della neat area {AreaPicco(data)}")

z = np.linspace(a, b, len(span))
plt.plot(z ,span, color='blue')
plt.show()
