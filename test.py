#!/usr/bin/python3.7

import matplotlib.pyplot as pl
import numpy as np
from parser import Parser
from curve import Curve
import os

def test_alg(curve):
    discarded = curve.discard_three_sig()
    if len(discarded) == 0:
        return (0, 0)
    #print(a)

    times  = np.array([ o[0] for o in discarded ])
    #mags   = np.array([ o[1] for o in discarded ])   
    #errors = np.array([ o[2] for o in discarded ])

    time_mean = times.mean()
    time_std  = times.std()

    #print(time_std)
    return time_std, len(discarded)

error_threshold = 0.1                                               # represents maximum relative error to be included in curve

filename = "data/blgXXX_X_i_2425.dat"
test_parser = Parser("test")                                        # test object
test_data = test_parser.read_one_curve(filename)                    # data from @filename file
test_curve = Curve(test_data, error_threshold)                      # test object holding whole data

test_curve.plot()

pl.show()
#pl.savefig("test123.png")
pl.clf()


def plot_all_curves(dir):
    ''' Simple function that plots all curves
    located in 'data/' folder '''

    if dir not in os.listdir("visualization"):
        os.mkdir(f"visualization/{dir}")
    for filename in os.listdir('data/'):
        parser = Parser("test")                                    
        data = parser.read_one_curve("data/"+filename)
        curve = Curve(data, error_threshold)


        if curve.count != 0:                                       # aborts plotting if curve has no data
            std, count = test_alg(curve)
            if std < std_threshold and count > count_threshold:
                curve.plot()
                pl.savefig(f"visualization/{dir}/{filename[:-4:]}.png")
                pl.clf()
                print(curve.discarded_value)


std_threshold = 290
count_threshold = 30

#plot_all_curves(f"batch_alg_std{std_threshold}_count{count_threshold}")