import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit 

#calibrazione sistema di misura per la spettroscopia di ragggi x
#xdata = Am241, Na22 1, na22 2, cs137, co60
y_data = np.array([93.05, 680.5, 1644.3, 880.01, 1512.66, 1713.12, 49.29])
y_err = np.array([0.05, 0.07,0.24,0.12, 0.46, 0.45, 0.02])
x_data = np.array([60, 511, 1274, 662, 1174, 1332, 31 ])

def linear(x, a, b):
    return a*x + b

#fit dei minimi quadrati
x= np.linspace(0, max(x_data), max(x_data))
popt, pcov= curve_fit(linear,x_data, y_data)
a_fit, b_fit  = popt

for i in range(len(y_data)):
    chi_square = np.sum((linear(x_data, a_fit, b_fit)[i]- y_data[i])**2/y_err[i]) #va diviso per gli errori 

dof = len(y_data) - len(popt)
chi_norm = chi_square / dof

print("---------")
print(f"Parametri del fit {popt}")
print(f"il chi2 è {chi_square} \nil chi normalizzato è {chi_norm}")
print("---------")



plt.errorbar(x_data, y_data, y_err, color="red", fmt="o")
plt.plot(x, linear(x, *popt), color="blue")
plt.xlabel("Energia [KeV]")
plt.ylabel("Posizione picco MCA [adm]")
plt.legend(title =f"a = {np.round(a_fit,3)}+-{np.round(np.sqrt(pcov[0,0]),3)}\nb = {np.round(b_fit,3)}+-{np.round(np.sqrt(pcov[1,1]),3)}")
plt.xlim(0,)
plt.ylim(0,)
plt.grid()
plt.show()

