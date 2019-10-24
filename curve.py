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
        self.discarded_value = 0


        if self.count != 0:
            self.mean_mag = self.mags.mean()
            self.mean_weighted_mag = sum(self.mags/(self.errors**2))/sum(1/self.errors**2)
            self.std_dev = self.mags.std()
        else:
            self.mean_mag = 0
            self.mean_weighted_mag = 0
            self.std_dev = 0
        

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

    
    def discard_three_sig(self):
        discarded = []
        _sum = 0
        #data = self.data
        for entry in self.data:
            div = abs(entry[1] - self.mean_mag)
            #print(f"{self.std_dev} | {div}")
            if div > 3 * self.std_dev:
                discarded.append(entry)
                _sum += div

        #self.update_data(data)
        self.discarded_value = _sum/(len(discarded)+1)
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


    def plot(self):
        ''' This method is responsible for plotting
        signle curve. '''
        
        pl.plot(self.times, self.mags, 'o', markersize=0.4)
        #pl.hlines(self.mean_weighted_mag, self.times[0], self.times[-1], \
        #          colors='g', label='weighted mean', linewidth=0.5)
        pl.hlines(self.mean_mag, self.times[0], self.times[-1], \
                  colors='r', label='mean', linewidth=0.5)
        for i in range(1, 4):
            pl.hlines(self.mean_mag + self.std_dev * i, self.times[0], self.times[-1], \
                      colors='y', linewidth=0.5 - i/10)
            pl.hlines(self.mean_mag + self.std_dev * (-i), self.times[0], self.times[-1], \
                      colors='y', linewidth=0.5 - i/10)
        pl.legend()