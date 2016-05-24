import os
import pandas as pd 




if __name__ == '__main__':
    

    folders = [
        '../data/resale-flat-prices-2', 
        '../data/resale-flat-prices-3'
    ]

    files = []
    for fld in folders:
        files += [ os.path.join(fld, f) for f in os.listdir(fld) if '.csv' in f]

    data = pd.concat(map(pd.read_csv, files))
    data['address'] = 'Blk ' + data.block + ', ' + data.street_name + ', Singapore'


    # Generate the basic raw file
    data.to_csv('../data/relaseData.csv', index=False)

    # Let us now create the data for Geotagging
    uniqueAddresses = {
        'address' : list(data['address'].unique())
    }

    uniqueAddresses = pd.DataFrame(uniqueAddresses)
    uniqueAddresses['tagged'] = False
    uniqueAddresses['lat'] = None
    uniqueAddresses['lng'] = None
    uniqueAddresses['full'] = None


    uniqueAddresses.to_csv('../data/uniqueAddresses.csv', index=False)



    print 'done'
