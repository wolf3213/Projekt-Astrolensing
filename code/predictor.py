import numpy as np

class Predictor:

    error_threshold = 0.1
    std_threshold   = 30
    count_threshold = 5
    width           = 3

    @staticmethod
    def starboy(curve, time_std_thr = std_threshold, count_thr = count_threshold):
        ''' Algorithm proposed by Rafał.
            How it works:
            -calculate mean magnitudo, magnitudo standard devaition
            -discard points which are widht*mag_std away from mean magnitudo
            -calculate (weighted) mean time of points which were discarded 
            -calculate time standard deviation (dispersion of discarded points, time-wise)
            -compare calculated values with thresholds:
                ~time_std_min is minimal time dispersion, prevents from returning predicting
                 too fast curve (1-2 days, we know lenses are wider)
                ~time_std_thr is maximal time dispersion, we know lenses are not wider 
                 than about 100-200 days
                ~count_thr is number of discarded points, we want curves that have
                 at least over a dozen points '''

        minimal_count = 1   
        time_std_min = 1            

        discarded = curve.discard_n_sig(Predictor.width)
        count = len(discarded)

        if count <= minimal_count: return False        # prevents from calculating mean over empty set

        curve.time_mean = Predictor.calculate_weighted_time_mean(curve, discarded)
        curve.time_std  = discarded[:, 0].std()
        curve.discarded_count = count

        found = curve.time_std > time_std_min and \
                curve.time_std < time_std_thr and \
                count > count_thr

        return found


    @staticmethod
    def calculate_weighted_time_mean(curve, discarded):
        ''' Calculates mean time for discarded points, but with
            weights. Weight is calculated by following formula:
            w_i = (mag[i] - mag_mean)^n1 / error[i]^n2 '''
        
        n1 = 2
        n2 = 2

        dist_from_mean = np.array([ curve.mag_mean - i[1] for i in discarded])
        errors = discarded[:, 2]/curve.mag_mean
        weights = dist_from_mean**n1 / errors**n2
        times = discarded[:, 0]

        return sum(times * weights) / sum(weights) 
    

    @staticmethod
    def predict_test_v2(curve):
        
        ''' Algorithm proposed by Adam.
        Idea
        To be close means disctance beetween two times has to be smaller than close_gap.
        Then number of close elements is contained in how_much set.
        It gives positive result when any element of how_much set is bigger than minclose.
        Numbers of positve results is ,,pos''
        Ex. 1,2,3,4,5,11,12,13,14,21,30
        close gap=1.1
        minclose=3
        Supposed result
        How much=[5,4,1,1]
        pos=3 '''
       
        times = np.array([o[0] for o in curve.discarded])
        how_much=[] #array containg numbers of close elements in order
        k=0 #just a variable
        pos=0
        close_gap=3
        minclose=16
        for i in range(1, len(times)): # i want iteriate over every element in times
            if(times[i]-times[i-1] <= close_gap):
                k+=1
            else:
                how_much.append(k)
                k=0
        for i in range(len(how_much)):   # i want iteriate over every element in how_much
            if(how_much[i] >= minclose):
                pos+=1
        #if(pos>=1): print(how_much)
        return pos >= 1

        #if (pos >=1): return True #true means lens founded
        # else: return False 
