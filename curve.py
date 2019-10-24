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
        self.mean_discarded_value = 0

        if self.count != 0:
            self.mean_mag = self.mags.mean()
            self.mean_weighted_mag = sum(self.mags/(self.errors**2))/sum(1/self.errors**2)
            self.std_dev = self.mags.std()
            self.max_mag = max(self.mags)
            self.min_mag = min(self.mags)
        else:
            self.mean_mag = 0
            self.mean_weighted_mag = 0
            self.std_dev = 0
            self.max_mag = 0
            self.min_mag = 0

        self.data = filtered
        
        self.filter_large_errors(threshold)


    def filter_nines(self, data, error_threshold):
        ''' Function removing entries that mag
            is higher than 99, which occurs alot, 
            also filters entries with high relative 
            error. '''

        result = []
        for entry in data:
            if not entry[1] > 99:
                result.append(entry)

        return result


    def filter_large_errors(self, error_threshold = 0.1):
        ''' Removes data entries from object, that have 
            relative error greater than given as an argument '''
        
        result = []
        for entry in self.data:
            if not entry[2]/self.mean_mag > error_threshold:
                result.append(entry)

        self.update_data(result)

    
    def discard_n_sig(self, n):
        ''' Returns set of data entries, that has magnitudo 
            value away from mean magnitudo by n*std '''

        discarded = []
        _sum = 0

        for entry in self.data:
            div = entry[1] - self.mean_mag
            
            if div < -n * self.std_dev:
                discarded.append(entry)
                _sum += div

        self.mean_discarded_value = _sum/(len(discarded)+1)

        return discarded


    def update_data(self, data):
        ''' This function updates object, should 
        be used whenever some entries should be 
        filtered '''

        self.times  = np.array([ o[0] for o in data ])
        self.mags   = np.array([ o[1] for o in data ])
        self.errors = np.array([ o[2] for o in data ])
        self.data = data
        self.count = len(data)

        if self.count != 0:
            self.mean_mag = self.mags.mean()
            self.mean_weighted_mag = sum(self.mags/(self.errors**2))/sum(1/self.errors**2)
            self.std_dev = self.mags.std()
        else:
            self.mean_mag = 0
            self.mean_weighted_mag = 0
            self.std_dev = 0


    def plot(self, mean = True, errors = True, t_min = 0, t_max = 0, t_mean = None):
        ''' This method is responsible for plotting
        signle curve. '''

        if t_min == 0: t_min = self.times[0]
        if t_max == 0: t_max = self.times[-1]

        height = self.min_mag  
        pl.plot(self.times, self.mags, 'o', markersize=0.4)

        if mean:
            pl.hlines(self.mean_mag, t_min, t_max, \
                    colors='g', label='mean', linewidth=0.5)
            for i in range(1, 4):
                pl.hlines(self.mean_mag + self.std_dev * i, t_min, t_max, \
                        colors='y', linewidth=0.5 - i/10)
                pl.hlines(self.mean_mag + self.std_dev * (-i), t_min, t_max, \
                        colors='y', linewidth=0.5 - i/10)

        if errors:
            pl.plot(self.times, self.errors + height, 'o', markersize=0.3, label='errors')
            pl.hlines(height, t_min, t_max, colors='r', linewidth=0.5, label='Zero error level')

        if t_mean is not None:
            pl.axvline(x=t_mean, color='r', linewidth='0.4', label='Predicted lens peak')
        
        pl.xlim((t_min, t_max))
        pl.legend()