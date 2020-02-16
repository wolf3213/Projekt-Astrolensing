class Parser:
    def __init__(self, filename, threshold=0.2, folder=False):
        """ This class is used to read files. "filename" should 
            be interpreted as filename, or as directory name,
            if "folder" is set to true """

        self.filename = filename
        self.threshold = threshold
        

    def read_one_curve(self, filename):
        """ Method responsible for reading data from single file.
            'filename' argument is just path to file, note that 
            you should enter relative or absolute path, f.ex. If file is 
            in 'data/_filename_', you should give 'data/_filename_' as 
            input to this method """

        data = []
        with open(filename, 'r') as f:
            try:
                data = f.read().split("\n")                         # data array is filled with strings , ex: "3900.53154 18.997 0.167 11  0 A"
            except:
                print(filename)
                return [ (_, 0, 0) for _ in range(2418) ]
                pass
            data = [ o.split() for o in data ]                  # converting strings to lists,        ex: ['3900.53154', '18.997', '0.167', '11', '0', 'A']
            data.pop()                                          # removes last, empty list from data array

        data = [ ( float(record[0]), \
                   float(record[1]), \
                   float(record[2]) ) for record in data]       # casts each entry from string to float, ignores last 3 values (what are they tho??)
        
        return data
