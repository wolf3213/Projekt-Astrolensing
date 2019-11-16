import numpy as np

class Predictor:

    error_threshold = 0.1  
    std_threshold   = 200
    count_threshold = 5
    width           = 3
    value_threshold = 10**3

    @staticmethod
    def predict_test(curve, std_thr = std_threshold, count_thr = count_threshold):
        #pls add coment here 
        minimal_count = 1   
        std_min = 1            

        discarded = curve.discard_n_sig(Predictor.width)
        count = len(discarded)

        if count <= minimal_count: return False        # prevents from calculating mean over empty set


        times   = np.array([ o[0] for o in discarded ])
        #mags   = np.array([ o[1] for o in discarded ])   
        #errors = np.array([ o[2] for o in discarded ])

        time_mean = times.mean()
        curve.time_mean, curve.some_value = Predictor.calculate_weighted_time_mean(curve, discarded)
        curve.time_std  = times.std()
        curve.discarded_count = count

        found = curve.time_std > std_min and curve.time_std < std_thr and count > count_thr and curve.some_value > Predictor.value_threshold
        return found


    @staticmethod
    def calculate_weighted_time_mean(curve, discarded):
        ''' Calculates mean time for discarded points, but with
            weights. Weight is calculated by following formula:
            w_i = (mag[i] - mag_mean)^2 / error[i]^2 '''
        dist_from_mean = np.array([ curve.mag_mean - i[1] for i in discarded])
        errors = discarded[:,2]/curve.mag_mean
        weights = dist_from_mean**3 / errors**1
        times = discarded[:,0]

        return sum(times * weights) / sum(weights), sum(weights)
    
    @staticmethod
    def predict_test_v2(curve):

        ''' Idea
        To be close means disctance beetween two times has to be smaller than close_gap.
        Then number of close elements is contained in how_much set.
        It gives positive result when any element of how_much set is bigger than minclose.
        Numbers of positve results is ,,pos''
        Ex. 1,2,3,4,5,11,12,13,14,21,30
        close gap=1.1
        minclose=3
        Supposed result
        How much=[5,4,1,1]
        pos=3 
	we can also add if which discards points below medium '''
        discarded = curve.discard_n_sig(2)
        times = np.array([o[0] for o in discarded])
        mags   = np.array([ o[1] for o in discarded ])   
        how_much=[1] #array containg numbers of close elements in order
        T=[] #array containg times which are ,,close'' 
        k=0 #just a variable
        pos=0
        close_gap=15.1
        minclose=7
        winmags=0
        for i in range(1, len(times)): # i want iteriate over every element in times 
            if(times[i]-times[i-1] <= close_gap and mags[i]< curve.mag_mean): #extended function now checks if y-axis also. 
                k+=1;T.append(times[i])
            else:
                how_much.append(k)
                k=0
       	for i in range(len(how_much)):   # i want iteriate over every element in how_much
            if(how_much[i] >= minclose):
                pos+=1
        #print(*how_much)
        for i in range(1, len(mags)):
            if(mags[i]<=curve.mag_mean-5*curve.mag_std):
                winmags+=1
        #print(winmags)
        #if(pos>=1)
        print("how_much") 
        print(*how_much)
        #print("czasy") 
        #print(*T) 
        #print("winmags") 
        print(winmags)
        print(pos)  
        return (pos >= 1 or winmags>=1)  

       
