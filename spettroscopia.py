import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

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
#eliminiamo il segnale di continuum dai dati

a = 774  #conteggi canale A
b = 979 #conteggi canale B
N_ch = b - a #conteggi fra A e B

ch_a = data[a]
ch_b = data[b]

def continum(ch_a, ch_b):
    return (ch_a + ch_b)*N_ch/2

y_data = data[a : b]
def AreaPicco(y_data):
    return sum(y_data) - continum(ch_a, ch_b)

print(f"Questa è la stima dell'area del continum {continum(ch_a, ch_b)} \nQuesta della neat area {AreaPicco(data)}")

channels = np.linspace(a, b, len(y_data))
#plt.plot(channels ,y_data, color='blue')
#plt.show()

#statistica poissoniana per ogni bin
y_err = np.sqrt(y_data)
y_err[y_err == 0] = 1

#funzione di fit gaussiana

def Gaussian(x,a,b,sigma):
    return a*np.exp(-(x-b)**2/(2*(sigma**2)))

#fit e test del chi quadro
popt, pcov = curve_fit(Gaussian, channels, y_data, p0 = [10, 800, 150])
a_fit, b_fit , sigma_fit = popt

y_fit = Gaussian(channels, *popt)
residuals = y_data - y_fit
for i in range(len(y_data)):
    chi_square = np.sum((residuals[i]/y_err[i])**2) #va diviso per gli errori 

dof = len(channels) - len(popt)
chi_norm = chi_square / dof

print("---------")
print(f"il chi2 è {chi_square} \nil chi normalizzato è {chi_norm}")
print("---------")

#plot del fit

plt.figure(figsize = (10,6))
plt.scatter(channels, y_data, label = "dati", color="purple", s=4)
plt.plot(channels, y_fit, label = "fit",color="red")
plt.xlabel("canali")
plt.ylabel("numero di eventi")
plt.legend()
plt.title(f"fit gaussiano per il picco del Cs137 ")
plt.show()