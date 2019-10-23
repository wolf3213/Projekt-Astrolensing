import numpy as np
import matplotlib.pyplot as pl

class Curve:
    def __init__(self, data, threshold=0.1):
        ''' This object is going to be basic data 
        structure. It will contain whole data for one 
        curve, which is one star '''

        filtered = self.filter_nines(data, threshold)
        self.times  = np.array([ o[0] for o in filtered ])   # array of times, in julian days
        self.mags   = np.array([ o[1] for o in filtered ])   # array of magnitudos, in mag
        self.errors = np.array([ o[2] for o in filtered ])   # array of measurement errors
        self.count = len(filtered)

        if self.count != 0:
            self.mean_mag = self.mags.mean()
            self.mean_weighted_mag = sum(self.mags/(self.errors**2))/sum(1/self.errors**2)
        else:
            self.mean_mag = 0
            self.mean_weighted_mag = 0
        

        self.data = filtered

    def filter_nines(self, data, error_threshold):
        ''' Function removing entries that mag
        is higher than 99, which occurs alot, 
        also filters entries with high relative 
        error. '''

        result = []
        for entry in data:
            if not entry[1] > 99 and \
               not entry[2]/entry[1] > error_threshold:
                result.append(entry)

        return result

    def update_data(self, data):
        ''' This function updates object, should 
        be used whenever some entries should be 
        filtered '''

        self.times  = [ o[0] for o in data ]
        self.mags   = [ o[1] for o in data ]
        self.errors = [ o[2] for o in data ]
        self.data = data


    def plot(self):
        ''' This method is responsible for plotting
        signle curve. '''
        
        pl.plot(self.times, self.mags, 'o', markersize=0.4)
        pl.hlines(self.mean_weighted_mag, self.times[0], self.times[-1], \
            colors='g', label='weighted mean', linewidth=0.5)
        pl.hlines(self.mean_mag, self.times[0], self.times[-1], \
            colors='r', label='mean', linewidth=0.5)
        pl.legend()