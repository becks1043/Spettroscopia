import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

class DataLoader:
    def __init__(self, file_path1):
        self.file_path1 = file_path1
    def load_data(self):
        data = []
        with open(self.file_path1, 'r' , encoding='utf-8', errors= 'replace') as file1:
            for linea1 in file1: 
                try:
                    if linea1:
                        risultato1 = int(linea1.strip())
                        data.append(risultato1)
                except ValueError:
                #righe_str.append(numero)
                    continue
        
        data = data[: -5]
        return data
    
class SpectralVisualiser:
    def __init__(self, x_data, y_data):
        self.x_data = x_data
        self.y_data = y_data
        
    def picture(self):
        plt.plot(self.x_data ,self.y_data, color='green')
        plt.xlabel("Canali")
        plt.ylabel("Numero di eventi")
        plt.xlim(0, len(self.y_data))
        plt.ylim(0,)
        plt.show()

class FrameworkChannels:
    def __init__(self, x_data, y_data):
        self.x_data = x_data
        self.y_data = y_data

    def range(self, channel_a, channel_b):
        if not isinstance(channel_a, int):
            raise ValueError("il canale A deve essere un numero intero")
        if not isinstance(channel_b, int):
            raise ValueError("il canale B deve essere un numero intero")
        x_selected = self.x_data[ channel_a : channel_b]
        y_selected = self.y_data[ channel_a : channel_b]
        return x_selected , y_selected
    
    def pictures(self, channel_a, channel_b):
        x_selected, y_selected = self.range(channel_a, channel_b)
        plt.scatter(x_selected, y_selected)
        plt.xlabel("Canali")
        plt.ylabel("Numero di eventi")
        plt.show()

    def gaussian_fit(self, channel_a, channel_b, sub_a, sub_b):
        x_selected , y_selected = self.range(channel_a, channel_b)
        #statistica poissoniana per ogni bin
        y_err = np.sqrt(y_selected)
        y_err[y_err == 0] = 1

        #sottraiamo il background
        N_ch = channel_b -channel_a

        def continum(ch_a, ch_b):
            return (ch_a + ch_b)*N_ch/2
        def AreaPicco(y_selected):
            return sum(y_selected) - continum(channel_a, channel_b)


        def linear_background(x,a,b):
            return a*x + b

        sub_a = 250
        sub_b = 500
        range_linear = self.y_data[sub_a:sub_b]
        x_range = np.linspace(sub_a,sub_b,len(range_linear))
        popt, pcov = curve_fit(linear_background, x_range ,range_linear)
        y_selected = [float(x) for x in y_selected]
        background_fit = linear_background(x_selected, *popt)
        y_selected -= background_fit

        plt.scatter(x_selected, y_selected)

        #funzione di fit gaussiana

        def Gaussian(x,a,b,sigma):
            return a*np.exp(-(x-b)**2/(2*(sigma**2)))

        #fit e test del chi quadro
        popt, pcov = curve_fit(Gaussian, x_selected, y_selected, p0 = [10, 800, 150],bounds=([0, -np.inf, 0], [np.inf, np.inf, np.inf]))
        a_fit, b_fit , sigma_fit = popt

        y_fit = Gaussian(x_selected, *popt)
        residuals = y_selected - y_fit
        for i in range(len(y_selected)):
            chi_square = np.sum((residuals[i]/y_err[i])**2) #va diviso per gli errori 

        dof = len(x_selected) - len(popt)
        chi_norm = chi_square / dof

        print("---------")
        print(f"Parametri del fit {popt}")
        print(f"il chi2 è {chi_square} \nil chi normalizzato è {chi_norm}")
        print("---------")

        #troviamo il picco e stimiamo l'errore
        peak_position = b_fit
        delta_peak_position = sigma_fit/ np.sqrt(AreaPicco(y_selected))
        print(f"La posizione del picco è {peak_position} +/- {delta_peak_position} \n---------")

        #plot del fit

        plt.figure(figsize = (10,6))
        plt.grid()
        plt.scatter(x_selected, y_selected, label = "dati", color="purple", s=4)
        #plt.errorbar(channels, y_data , yerr=y_err ,fmt='.')
        plt.plot(x_selected, y_fit, label = "fit",color="red")
        plt.xlabel("Canali")
        plt.ylabel("Numero di eventi")
        plt.legend()
        plt.title(f"Fit gaussiano per il picco")
        plt.show()


