#!/usr/bin/python3.7

import matplotlib.pyplot as pl
import numpy as np
from parser import Parser
from curve import Curve
import os

def test_alg(curve):
    discarded = curve.discard_n_sig(2)
    if len(discarded) < 2:
        return (0, 0, 0)

    times   = np.array([ o[0] for o in discarded ])
    #mags   = np.array([ o[1] for o in discarded ])   
    #errors = np.array([ o[2] for o in discarded ])

    time_mean = times.mean()
    time_std  = times.std()

    return time_mean, time_std, len(discarded)


def plot_all_curves(dir):
    ''' Simple function that plots all curves
    located in 'data/' folder '''

    if dir not in os.listdir("visualization"):
        os.mkdir(f"visualization/{dir}")
    if dir not in os.listdir("curves"):
        os.mkdir(f"curves/{dir}")
    for filename in os.listdir('data/'):
        parser = Parser("test")                                    
        data = parser.read_one_curve("data/"+filename)
        curve = Curve(data, error_threshold)


        ''' this part below should be in separate function '''
        if curve.count != 0:                                            # aborts plotting if curve has no data
            mean, std, count = test_alg(curve)
            if std < std_threshold and count > count_threshold:

                curve.plot(t_mean = mean)                               # plots whole curve, saves to file in visualization/dir/
                pl.savefig(f"visualization/{dir}/{filename[:-4:]}.png") 
                pl.clf()

                curve.plot(t_min = mean - std/2, \
                           t_max = mean + std/2, t_mean = mean)         # plots only interesting are, saves to file in curves/dir
                pl.savefig(f"curves/{dir}/{filename[:-4:]}.png")
                pl.clf()

                print(mean, std, count, curve.mean_discarded_value)     # prints parameters


if __name__ == "__main__":
    error_threshold = 0.05                                              # represents maximum relative error to be included in curve

    filename = "data/photBLG100.1.I.102672.dat"                         # reference lens
    test_parser = Parser("test")                                        # test object
    test_data = test_parser.read_one_curve(filename)                    # data from @filename file
    test_curve = Curve(test_data, error_threshold)                      # test object containing whole data

    mean, std, count = test_alg(test_curve)
    print(mean, std, count, test_curve.mean_discarded_value)

    test_curve.plot(t_mean=mean)

    pl.show()
    pl.clf()

    std_threshold = 200
    count_threshold = 4

    plot_all_curves(f"batch_alg_std{std_threshold}_count{count_threshold}")