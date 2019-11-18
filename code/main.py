#!/usr/bin/python3.7
#from predictor import Predictor
from utilities import *


if __name__ == "__main__":


    print(f"Relative error threshold: {Predictor.error_threshold}\
         \nTime standard deviation threshold: {Predictor.std_threshold}\
         \nNumber of discarded points threshold: {Predictor.count_threshold}\
         \nNumber of standard deviations to discard: {Predictor.width}")

    filename = "zadanie1/blgXXX_X_i_80418.dat"
    directory = 'zadanie1/'


    #Tools.run_starboy_single(filename)
    Tools.run_starboy_batch(directory)





'''
    REFERENCE LENSES

    #filename = "data/photBLG100.1.I.124027.dat"                                # reference lenses
    #filename = "data/photBLG100.1.I.160378.dat"
    #filename = "data/photBLG100.1.I.119596.dat"
    #filename = "data/photBLG100.1.I.106173.dat"
    #filename = "data/photBLG100.1.I.102672.dat"
    #filename = "data/photBLG100.1.I.101269.dat"
    #filename = "data/blgXXX_X_i_1086.dat"
    #filename = "zadanie1/blgXXX_X_i_27155.dat"

'''