class Parser:
    def __init__(self, filename, folder=False):
        """ THIS CLASS IS USED TO READ FILES. "FILENAME" SHOULD 
        BE INTERPRETED AS FILENAME, OR AS DIRECTORY NAME,
        IF "FOLDER" IS SET TO TRUE """
        pass
        

    def read_one_curve(self, filename):
        """ METHOD RESPONSIBLE FOR READING DATA FROM SINGLE FILE.
        'FILENAME' ARGUMENT IS JUST PATH TO FILE, NOTE THAT 
        YOU SHOULD GIVE WHOLE PATH, F.EX. IF FILE IS 
        IN 'DATA/_FILENAME_', YOU GIVE 'DATA/_FILENAME_ AS 
        INPUT TO THIS METHOD """

        data = []
        with open(filename, 'r') as f:
            data = f.read().split("\n")                         # data array is filled with strings , ex: "3900.53154 18.997 0.167 11  0 A"
            data = [ o.split() for o in data ]                  # converting strings to lists,        ex: ['3900.53154', '18.997', '0.167', '11', '0', 'A']
            data.pop()                                          # removes last, empty list from data array

        data = [ ( float(record[0]), \
                   float(record[1]), \
                   float(record[2]) ) for record in data]       # casts each entry from string to float, ignores last 3 values (what are they tho??)
        
        return data