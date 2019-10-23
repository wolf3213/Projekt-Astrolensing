#!/usr/bin/python3.7

import matplotlib.pyplot as pl
import numpy as np
from parser import Parser
from curve import Curve
import os

def test_alg(curve):
    pass

error_threshold = 0.1                                               # represents maximum relative error to be included in curve

filename = "data/blgXXX_X_i_1176.dat"
test_parser = Parser("test")                                        # test object
test_data = test_parser.read_one_curve(filename)                    # data from @filename file
test_curve = Curve(test_data, error_threshold)                      # test object holding whole data

test_curve.plot()

pl.show()
pl.clf()

def plot_all_curves(dir):
    ''' Simple function that plots all curves
    located in 'data/' folder '''

    os.mkdir(f"visualization/{dir}")
    for filename in os.listdir('data/'):
        parser = Parser("test")                                    
        data = parser.read_one_curve("data/"+filename)
        curve = Curve(data, error_threshold)

        if curve.count != 0:                                       # aborts plotting if curve has no data
            curve.plot()

        pl.savefig(f"visualization/{dir}/{filename[:-4:]}.png")
        pl.clf()

plot_all_curves("batch2")