import os
import pandas as pd
import numpy  as np
# import matplotlib.pyplot as plt
 
def tostoreyMean(strMean):
 
    return np.mean(map(float, strMean.replace('TO', '').split()))
 
def findCounts(data, featureGroups=['town', 'flat_model', 'flat_type', 'month'], fileName='findCounts.csv'):
 
    data['countCol'] = 1
    data[ ['countCol']+featureGroups ].groupby(featureGroups).agg(lambda m: m.count()).reset_index().to_csv(fileName, index=False)
 
    data.drop('countCol', axis=1)
 
    return
 
def plotItems():
 
    return
 
 
if __name__ == '__main__':
 
    # files = [os.path.join('data', f) for f in os.listdir('data') if '.csv' in f ]
    # data  = pd.concat(map(pd.read_csv, files))
 
    # # Transformations:
    # data.month = data.month.astype(np.datetime64)
    # data.storey_range = data.storey_range.map( tostoreyMean )

    # data = pd.read_csv('../data/relaseData.csv')
    # findCounts(data, fileName='../data/findCounts.csv')
 
    data1 = pd.read_csv('../data/findCounts.csv')   
    data1.months = data1.month.astype(np.datetime64)
    data1['flat'] = data1.flat_type + '#' + data1.flat_model
    towns = list(data1.town)
    # townColors = dict([ (t, plt.cm.spectral(  float(i)/(len(towns)-1) )   )   for i, t in enumerate(towns) ])
 
    # for k, df in data1.groupby('flat'):
    #     plt.figure()
    #     plt.scatter( data1.months, data1.countCol, c = data1.town.map( townColors ) )
 
    # plt.show()
 
    print 'done'
 