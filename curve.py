class Curve:
    def __init__(self, data):
        ''' This object is going to be basic data 
        structure. It will contain whole data for one 
        curve, which is one star '''

        filtered = self.filter_nines(data)
        self.times  = [ o[0] for o in filtered ]   # array of times, in julian days
        self.mags   = [ o[1] for o in filtered ]   # array of magnitudos, in mag
        self.errors = [ o[2] for o in filtered ]   # array of measurement errors

        self.data = filtered

    def filter_nines(self, data):
        ''' Function removing entries that mag
        is higher than 99, which occurs alot '''

        result = []
        for entry in data:
            if not entry[1] > 99:
                result.append(entry)

        return result

    def update_data(self, data):
        ''' This function updates object, should 
        be used whenever some entries should be 
        filtered '''
        
        self.times  = [ o[0] for o in data ]
        self.mags   = [ o[1] for o in data ]
        self.errors = [ o[2] for o in data ]
        self.data = data

