#!/usr/bin/python3.7

import matplotlib.pyplot as pl
from parser import Parser

test_parser = Parser("test")                                        # test object
test_data = test_parser.read_one_curve("data/blgXXX_X_i_19.dat")    # data from 'blgXXX_X_i_19.dat' file

times = [ a[0] for a in test_data ]                                 # array of times, in julian days
mags  = [ a[1] for a in test_data ]                                 # array of magnitudos, in mag
errors    = [ a[2] for a in test_data ]                             # array of measurement errors

pl.plot(times, mags, 'o', markersize=0.4)
pl.show()