#!/usr/bin/python3.7
#from predictor import Predictor
from utilities import *
import os


if __name__ == "__main__":

    print(f"Relative error threshold: {Predictor.error_threshold}\
         \nTime standard deviation threshold: {Predictor.std_threshold}\
         \nNumber of discarded points threshold: {Predictor.count_threshold}\
         \nNumber of standard deviations to discard: {Predictor.width}")

    filename = "data/photBLG100.1.I.102672.dat" 
    filename = "data/photBLG100.1.I.102672.dat"
    #filename = "data/photBLG100.1.I.160378.dat"
    #filename = "zadanie1/blgXXX_X_i_226054.dat"
    #filename = "zadanie1/blgXXX_X_i_160378.dat"
    #filename = "zadanie1/blgXXX_X_i_17175.dat"
    #filename = "zadanie1/blgXXX_X_i_81466.dat"
    #filename = "zadanie1/blgXXX_X_i_173020.dat"
    #filename = "zadanie1/blgXXX_X_i_226054.dat"

    directory = 'zadanie1/'
    #directory = 'data/'

    #filename = "blgXXX_X_i_1086.png"

    #Tools.run_starboy_single(filename)
    Tools.run_starboy_batch(directory, out_directory='final')

    #for filename in os.listdir(directory):
    #    Tools.run_starboy_single(directory+filename)





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
