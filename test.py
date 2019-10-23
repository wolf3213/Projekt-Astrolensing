#!/usr/bin/python3.7

import matplotlib.pyplot as pl
from parser import Parser
from curve import Curve

test_parser = Parser("test")                                        # test object
test_data = test_parser.read_one_curve("data/blgXXX_X_i_19.dat")    # data from 'blgXXX_X_i_19.dat' file
test_curve = Curve(test_data)                                       # test object holding whole data

pl.plot(test_curve.times, test_curve.mags, 'o', markersize=0.4)
pl.show()