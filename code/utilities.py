import matplotlib.pyplot as pl
import numpy as np
from parser import Parser
from curve import Curve
from predictor import Predictor
import os

class Tools:


    @staticmethod
    def open_and_parse_files(dir):
        ''' Function that opens .dat files and parses them 
            to our Curve object. Do not use on very large 
            data sets, it loads all of curves to memory 
            so this can take very long time and potentially 
            crash. '''

        parser = Parser("test")
        curves = []

        for filename in os.listdir(dir):                                    
            data = parser.read_one_curve(dir+filename)
            curve = Curve(data, filename[5:-4:], Predictor.error_threshold)
            curves.append(curve)

        return curves
    

    @staticmethod
    def run_starboy_batch(curves_directory, out_directory = "test_dir"):
        ''' Function that runs our starboys algorithm over 
            folder specified in 'curves_directory' string. 
            It reads and classifies curves in real time, may take
            some time on large data set. Starboy algorithm is described
            in Predictor class. '''

        dir = f"std{Predictor.std_threshold}_n{Predictor.width}_count{Predictor.count_threshold}"
        if out_directory != "test_dir":
            dir = out_directory

        if dir not in os.listdir("visualization"):
            os.mkdir(f"visualization/{dir}")
        if dir not in os.listdir("curves"):
            os.mkdir(f"curves/{dir}")

        parser = Parser("test")

        for filename in os.listdir(curves_directory):                                    
            data = parser.read_one_curve(curves_directory+filename)
            name = filename.split(".")[-2]
            curve = Curve(data, name, Predictor.error_threshold)
        
            if Predictor.starboy(curve):
                
                curve.plot(t_mean = curve.time_mean)                    # plots curve, saves to file in visualization/dir/
                pl.savefig(f"visualization/{dir}/{curve.name}.png") 
                pl.clf()

                print(curve)


    @staticmethod
    def run_starboy_single(filename):
        ''' Function that runs starboy algorithm on one 
            curve (to calculate predicted peak), and also
            plots one. '''

        parser = Parser("test")                                           # parser object
        data = parser.read_one_curve(filename)                            # data from @filename file
        name = filename.split(".")[-2]
        curve = Curve(data, name, Predictor.error_threshold)   # object containing star's data
        predicted = Predictor.starboy(curve)
        print(predicted)

        curve.gauss_dif()

        curve.plot(t_mean=curve.time_mean, gauss=True)

        pl.show()
        pl.clf()
