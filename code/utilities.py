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
            name = filename.split(".")[-2].split("_")[-1]
            curve = Curve(data, name, Predictor.error_threshold)
            curve.cut_points([0, 2137], [2450, 2500])
        

            if Predictor.starboy(curve):
                
                p = curve.fit()

                curve.plot(t_mean = curve.time_mean)                    # plots curve, saves to file in visualization/dir/
                pl.savefig(f"visualization/{dir}/{curve.name}.png") 
                pl.clf()

                curve.plot(t_mean = curve.time_mean, t_std=True, only_lens=True)                    # plots curve, saves to file in visualization/dir/
                x = np.arange(curve.times[0], curve.times[-1], 0.1)
                pl.plot(x, Curve.paczynski(x, p[0], p[1], p[2], p[3], p[4]), label="Fitted Paczyński's curve")
                pl.savefig(f"curves/{dir}/{curve.name}.png") 
                pl.clf()

                print(curve)


    @staticmethod
    def run_starboy_single(filename):
        ''' Function that runs starboy algorithm on one 
            curve (to calculate predicted peak), and also
            plots one. '''

        parser = Parser("test")                                           # parser object
        data = parser.read_one_curve(filename)                            # data from @filename file
        name = filename.split(".")[-2].split('_')[-1]
        curve = Curve(data, name, Predictor.error_threshold)              # object containing star's data
        curve.cut_points([0, 2137], [2450, 2500])
        predicted = Predictor.starboy(curve)
        print(predicted)
        p = curve.fit()
        print(p)
        x = np.arange(curve.times[0], curve.times[-1], 0.1)
        pl.plot(x, Curve.paczynski(x, p[0], p[1], p[2], p[3], p[4]), color='orange', label="Fitted Paczyński's curve")

        curve.plot(t_mean=curve.time_mean, t_std=True, only_lens=False)

        print(curve)
        pl.show()
        pl.clf()
