import numpy as np
import matplotlib.pyplot as pl
from scipy.optimize import curve_fit


class Curve:
    def __init__(self, data, name, threshold=0.1):
        ''' This object is going to be basic data 
            structure. It will contain whole data for one 
            curve, which is one star '''

        self.name = name

        filtered = self.filter_nines(data)
        
        self.update_data(filtered)
        
        self.filter_large_errors(threshold)


    def update_data(self, data):
        ''' This function updates object, should 
            be used whenever some entries should be 
            filtered, also used to initalize all 
            neccesary fields. '''

        self.times  = np.array([ o[0] for o in data ])
        self.mags   = np.array([ o[1] for o in data ])
        self.errors = np.array([ o[2] for o in data ])
        self.data   = data
        self.count  = len(data)

        self.discarded                = []
        self.discarded_mag_mean_value = 0
        self.discarded_max            = 0
        self.discarded_count          = 0
        self.time_mean                = 0
        self.time_std                 = 0

        if self.count != 0:
            self.mag_mean = self.mags.mean()
            self.mag_weighted_mean = sum(self.mags/(self.errors**2))/sum(1/self.errors**2)
            self.mag_std = self.mags.std()
            self.mag_max = max(self.mags)
            self.mag_min = min(self.mags)
        else:
            self.mag_mean           = 0
            self.mag_weighted_mean  = 0
            self.mag_std            = 0
            self.mag_max            = 0
            self.mag_min            = 0

        self.dist_from_mean = self.mags - np.full(self.count, self.mag_mean)


    def fit(self):
        start_params = [self.time_mean, 0.5, self.time_std*3, 0.9, self.mag_mean]
        try:
            params, pcov = curve_fit(Curve.paczynski, self.times, self.mags, p0=start_params)
        except RuntimeError:
            params = start_params
        #print (pcov)
        params_dict = {"Time":params[0], "Distance (in rE)":params[1], "Duration":abs(params[2]),
                       "Blending":params[3], "Base mag":params[4]}
        return params_dict


    def cut_points(self, *args):
        ''' opis
            '''

        result = []
        for entry in self.data:
            control = False
            for r in args:
                if (entry[0] > r[0] and entry[0] < r[1]):
                    control = True
                    
            if not control:
                result.append(entry)

        self.update_data(result)
        return result


    def filter_nines(self, data):
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
            if not entry[2]/self.mag_mean > error_threshold:
                result.append(entry)

        self.update_data(result)

    
    def discard_n_sig(self, n):
        ''' Returns set of data entries, that has magnitudo 
            value away from mean magnitudo by n*std '''

        discarded = []
        _sum = 0

        for entry in self.data:
            dif = entry[1] - self.mag_mean
            
            if dif < -n * self.mag_std:
                discarded.append(entry)
                _sum += dif

        self.discarded = discarded
        if len(discarded) == 0: return np.array([])

        self.discarded_mag_mean_value = _sum/(len(discarded)+1)
        self.discarded_max = min([e[1] for e in discarded])

        return np.array(discarded)


    @staticmethod
    def paczynski(t, t0, u0, te, fs, mb):
        ''' opis 
            '''

        u = np.sqrt( ((t-t0)/te)**2 + u0 )
        miu = (u**2 + 2) / (u * np.sqrt(u**2+4))
        mag = mb - 2.5 * np.log10(fs * (miu-1) + 1)
        return mag


    def gauss(self, x):
        ''' Only for some testing '''

        g = abs(self.discarded_max-self.mag_mean)*np.exp(-(x - self.time_mean)**2/4*self.mag_std**2)#/(self.mag_std*(2*np.pi)**0.5)
        return self.mag_mean - g   

    
    def fit_dif(self, fit, *params, only_lens = False):
        ''' Testing concept, will describe later (or not)
            if idea won'r work (which is what's going to happen propably) '''

        if not only_lens:
            t_min = self.times[0]
            t_max = self.times[-1]
        else:
            t_min = self.time_mean - 3*self.time_std
            t_max = self.time_mean + 3*self.time_std

        indices1 = self.times >= t_min
        indices2 = self.times <= t_max

        indices = indices1 & indices2

        dif = (self.mags[indices] - fit(self.times[indices], *params))**2/self.errors[indices]**2

        return np.sum(dif)/(len(indices)-5)


    def __repr__(self):
        return f"time_mean:{self.time_mean:.1f}|time_std:{self.time_std:.1f}|disc_count:{self.discarded_count}|name:{self.name}"


    def plot(self, mean = True, errors = False, gauss = False, only_lens = False, t_mean = None, t_std = False):
        ''' This method is responsible for plotting
            single curve. '''

        if not only_lens:
            t_min = self.times[0]
            t_max = self.times[-1]
        else:
            t_min = self.time_mean - 3*self.time_std - 75
            t_max = self.time_mean + 3*self.time_std + 75

        pl.plot(self.times, self.mags, 'o', markersize=0.7)

        if errors:
            pl.errorbar(self.times, self.mags, yerr=self.errors, fmt='o', linewidth=0.4, ms=1, zorder=1)

        if mean:
            pl.hlines(self.mag_mean, t_min, t_max, \
                    colors='g', label='Mean', linewidth=0.5)
            for i in range(1, 4):
                pl.hlines(self.mag_mean + self.mag_std * i, t_min, t_max, \
                        colors='y', linewidth=0.5 - i/10)
                pl.hlines(self.mag_mean + self.mag_std * (-i), t_min, t_max, \
                        colors='y', linewidth=0.5 - i/10)
        
        if gauss:
            x = np.arange(self.times[0], self.times[-1], 0.1)
            pl.plot(x, self.gauss(x), linewidth=0.4)

        if t_mean is not None:
            pl.axvline(x=t_mean, color='r', linewidth='0.4', label='Predicted peak')

        if t_std:
            pl.axvline(x=t_mean + 3*self.time_std, color='y', linewidth='0.4')
            pl.axvline(x=t_mean - 3*self.time_std, color='y', linewidth='0.4')

        pl.xlabel("Time [days]")
        pl.ylabel("Intensitivity [mag]")
        pl.title(self.name)
        pl.xlim((t_min, t_max))
        pl.gca().invert_yaxis()
        pl.legend()
