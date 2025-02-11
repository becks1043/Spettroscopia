import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from PROGETTO_classe import DataLoader

file_names = ['Cs137_135mm.Spe', 'Cs137_195mm.Spe', 'Cs137_255mm.Spe', 'Cs137_314mm.Spe', 'Cs137_375mm.Spe']

a = 780 #conteggi canale A
b = 970 #conteggi canale B
N_ch = b - a #conteggi fra A e B

def continum(Na, Nb):
    return (Na + Nb)*N_ch/2

def AreaPicco(y_data, a, b):
        return sum(y_data) - continum(y_data[a], y_data[b])


area_peak = []
for i in range(len(file_names)):
    loader = DataLoader(file_names[i])
    y_data = loader.load_data()
    area = AreaPicco(y_data, a, b)
    area_peak.append(area)

print(area_peak)
