import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

data_name = "Na22.Spe"
background_name = "fondo.Spe"
#diamo una struttura dati al nostro file di acquisizione
data = []
background = []

#NOTA il file aveva un carattere speciale orrendo --> errors= replace crea una istanza e  risolve il problema
#apro i dati con open()
with open(data_name, 'r' , encoding='utf-8', errors= 'replace') as file1, open(background_name, 'r' , encoding='utf-8', errors= 'replace') as file2:
    for linea1, linea2 in zip(file1, file2): 
            try:
                if linea1:
                    risultato1 = int(linea1.strip())
                    data.append(risultato1)
            except ValueError:
                #righe_str.append(numero)
                continue
            try:
                if linea2:
                    risultato2 = int(linea2.strip())
                    background.append(risultato2)
            except ValueError:
                #righe_str.append(numero)
                continue


data = data[: -5]
background = background[:-2]

print(f'La shape del tensore dei dati è {np.shape(data)}, il numero dei canali è {np.shape(data)[0]}') #occhio alle tuple!

#creiamo l'istogramma
bins = np.shape(data)[0]
#plt.hist(data, bins, edgecolor='blue', facecolor='none')

x = np.linspace(0, bins, bins)
plt.plot(x ,data, color='green')
plt.xlabel("Canali")
plt.ylabel("Numero di eventi")
plt.xlim(0, 2048)
plt.ylim(0,)
plt.show()
 
print("--------")
#eliminiamo il segnale di continuum dai dati

a = 630 #conteggi canale A
b = 730 #conteggi canale B
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
#statistica poissoniana per ogni bin
y_err = np.sqrt(y_data)
y_err[y_err == 0] = 1

#sottraiamo il background

def linear_background(x,a,b):
    return a*x + b

a1 = 250
b1 = 500
range_linear = data[a1:b1]
x_range = np.linspace(a1,b1,len(range_linear))
popt, pcov = curve_fit(linear_background,x_range ,range_linear)
data = [float(x) for x in data]
background_fit = linear_background(x, *popt)
y_data -= background_fit[a : b] 

plt.scatter(channels, y_data)

#funzione di fit gaussiana

def Gaussian(x,a,b,sigma):
    return a*np.exp(-(x-b)**2/(2*(sigma**2)))

#fit e test del chi quadro
popt, pcov = curve_fit(Gaussian, channels, y_data, p0 = [10, 800, 150],bounds=([0, -np.inf, 0], [np.inf, np.inf, np.inf]))
a_fit, b_fit , sigma_fit = popt

y_fit = Gaussian(channels, *popt)
residuals = y_data - y_fit
for i in range(len(y_data)):
    chi_square = np.sum((residuals[i]/y_err[i])**2) #va diviso per gli errori 

dof = len(channels) - len(popt)
chi_norm = chi_square / dof

print("---------")
print(f"Parametri del fit {popt}")
print(f"il chi2 è {chi_square} \nil chi normalizzato è {chi_norm}")
print("---------")

#troviamo il picco e stimiamo l'errore
peak_position = b_fit
delta_peak_position = sigma_fit/ np.sqrt(AreaPicco(y_data))
print(f"La posizione del picco è {peak_position} +/- {delta_peak_position} \n---------")

#plot del fit

plt.figure(figsize = (10,6))
plt.grid()
plt.scatter(channels, y_data, label = "dati", color="purple", s=4)
#plt.errorbar(channels, y_data , yerr=y_err ,fmt='.')
plt.plot(channels, y_fit, label = "fit",color="red")
plt.xlabel("Canali")
plt.ylabel("Numero di eventi")
plt.legend()
plt.title(f"Fit gaussiano per il picco del {data_name} ")
plt.show()