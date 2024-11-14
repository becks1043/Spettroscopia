import numpy as np
import spettroscopia
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

class DataFit:
    def __init__(self, x_data,y_data):
        self.x_data = x_data
        self.y_data = y_data
        self.range_x =(min(x_data), max(x_data))
        self.fit_params = None
        self.fit_function = None

    def set_range(self, x_min, x_max): #imposta il range
        self.range_x = (x_min, x_max)

    def select_data_in_range(self):
        mask = (self.x_data >= self.range_x[0]) & ( self.x_data <= self.range_x[1])
        return self.x_data[mask], self.y_data[mask]
    
    def fit_data(self, func):
        self.fit_function = func
        x_selected, y-selected = self.select_data_in_range()
        self.fit_params, _ = curve_fit