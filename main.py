#!/usr/bin/python3.7

import matplotlib.pyplot as pl
import numpy as np
from parser import Parser
from curve import Curve
from predictor import Predictor
import os


def plot_all_curves():
    ''' Simple function that plots all curves
    located in 'data/' folder '''

    dir = f"batch_alg_std{Predictor.std_threshold}_count{Predictor.count_threshold}"

    if dir not in os.listdir("visualization"):
        os.mkdir(f"visualization/{dir}")
    if dir not in os.listdir("curves"):
        os.mkdir(f"curves/{dir}")
    for filename in os.listdir('data/'):
        parser = Parser("test")                                    
        data = parser.read_one_curve("data/"+filename)
        curve = Curve(data, filename[5:-4:], Predictor.error_threshold)

        if Predictor.predict_test(curve, Predictor.std_threshold, Predictor.count_threshold):
            params = f"{curve.some_value:.0}|{curve.time_mean:.1f}|{curve.time_std:.1f}|{curve.discarded_count}|{filename[:-4:]}"
            
            curve.plot(t_mean = curve.time_mean)                               # plots whole curve, saves to file in visualization/dir/
            pl.savefig(f"visualization/{dir}/{filename[:-4:]}.png") 
            pl.clf()

            curve.plot(t_min = curve.time_mean - curve.time_std/2, \
                        t_max = curve.time_mean + curve.time_std/2, t_mean = curve.time_mean)         # plots only interesting are, saves to file in curves/dir
            pl.savefig(f"curves/{dir}/{filename[:-4:]}_{params}.png")
            pl.clf()

            #print(curve.time_mean, curve.time_std, curve.discarded_count, curve.some_value)     # prints parameters
            print(params)


if __name__ == "__main__":
    Predictor.error_threshold = 0.1                                                # represents maximum relative error to be included in curve
    Predictor.std_threshold   = 358
    Predictor.count_threshold = 5
    Predictor.width           = 3
    Predictor.value_threshold = 10**0

    print(f"Relative error threshold: {Predictor.error_threshold}\
         \n Time standard deviation threshold: {Predictor.std_threshold}\
         \n Number of discarded points threshold: {Predictor.count_threshold}\
         \n Number of standard deviations to discard: {Predictor.width}\
         \n Value threshold: {Predictor.value_threshold}")

    #filename = "data/photBLG100.1.I.124027.dat"                                # reference lens
    #filename = "data/photBLG100.1.I.160378.dat"
    #filename = "data/photBLG100.1.I.119596.dat"
    #filename = "data/photBLG100.1.I.106173.dat"
    #filename = "data/photBLG100.1.I.102672.dat"
    #filename = "data/photBLG100.1.I.101269.dat"
    filename = "data/blgXXX_X_i_1086.dat"

    test_parser = Parser("test")                                                # test object
    test_data = test_parser.read_one_curve(filename)                            # data from @filename file
    test_curve = Curve(test_data, filename[5:-4:], Predictor.error_threshold)   # test object containing whole data
    Predictor.predict_test_v2(test_curve)

    params = f"{test_curve.some_value:.0}|{test_curve.time_mean:.1f}|{test_curve.time_std:.1f}|{test_curve.discarded_count}|{filename[:-4:]}"
    print(params)

    #mean, std, count = test_alg(test_curve)
    #print(mean, std, count, test_curve.mean_discarded_value)

    test_curve.plot(t_mean=test_curve.time_mean)

    pl.show()
    pl.clf()

    plot_all_curves()
