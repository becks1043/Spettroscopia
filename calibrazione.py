import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
#in ordine na22 cs137 am124 ba113 co60

y_data = np.array([680.8, 880.1,92.73, 485.5 ,1513.2])
y_err = np.array([0.1, 0.1 ,0.04, 0.2, 0.6])
x_data = np.array([511, 662, 60, 356, 1174])



def linear(x,a,b):
    return a*x + b

popt, pcov = curve_fit(linear, x_data, y_data, p0 = None)
a_fit, b_fit  = popt

y_fit = linear(x_data, *popt)
residuals = y_data - y_fit
for i in range(len(y_data)):
    chi_square = np.sum((residuals[i]/y_err[i])**2) #va diviso per gli errori 

dof = len(x_data) - len(popt)
chi_norm = chi_square / dof
print(f"parametri del fit {popt}")

#plt.scatter(x_data, y_data, label = "dati", color="purple", s=4)
plt.errorbar(x_data, y_data, y_err, fmt='.', color='pink', ecolor="purple")
#plt.errorbar(channels, y_data , yerr=y_err ,fmt='.')
plt.plot(x_data, y_fit, label = "fit",color="red")
plt.xlabel("Energie")
plt.ylabel("Canali")
plt.legend()
plt.title(f"Calibrazione")
plt.show()