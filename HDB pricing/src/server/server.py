import bottle
import pandas as pd 
import json, os
import numpy as np 

app = bottle.Bottle()

def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        bottle.response.headers['Access-Control-Allow-Origin'] = '*'
        bottle.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        bottle.response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

@app.route('/')
def root():
    return 'This is the root application'

def jsonizeDf(df):
    '''
        Given a dataframe, this is going to convert the 
        dataframe to a jsonized string ...
    '''

    def changeCol(val):
        result = []
        try:    result = map(float, list(val))
        except: result = list(val)
        return result

    data = dict((c, changeCol( df[c] ) ) for c in df.columns)
    return json.dumps(data)

def dictizeDf(df):
    '''
        Given a dataframe, this is going to convert the 
        dataframe to a dictionary ...
    '''

    def changeCol(val):
        result = []
        try:    result = map(float, list(val))
        except: result = list(val)
        return result

    data = dict((c, changeCol( df[c] ) ) for c in df.columns)
    return data

def tostoreyMean(strMean):

    return np.mean(map(float, strMean.replace('TO', '').split()))

@app.route('/data/unique/<value>')
@enable_cors
def getUnique(value):

    fileName = '../../data/unique-%s.csv'%value
    if os.path.exists(fileName):
        data = list(pd.read_csv(fileName, header=None).ix[:,0])
        data = '["' + '","'.join(data) + '"]'
        return data
    else:
        return '[]'

    return

@app.route('/data/raw/columns')
@enable_cors
def columns():
    '''
        This just returns the columns in the current 
        dataframe. 
    '''
    columns = list(data.columns)

    return '["' + '","'.join(columns) + '"]'

@app.route('/data/raw', method='POST')
@enable_cors
def rawData():
    postdata  = bottle.request.body.read()
    postdata  = json.loads(postdata)

    for k in postdata:
        print 
        print k, ':', postdata[k]
        

    if postdata['x'] is None: return 'empty'
    if postdata['y'] is None: return 'empty'

    # Lets start by filtering the data ...
    temp = [ data[v2].isin(postdata[v1]) for (v1, v2) in zip(['flatTypeFilter', 'flatModelFilter', 'townFilter'], 
                                                             ['flat_type',      'flat_model',      'town']) ]
    rows = reduce(lambda m, n: m & n, temp)
    cols = [postdata[c] for c in ['x', 'y', 'gBy', 'gByI'] if (postdata[c] is not None) and (postdata[c] != 'None') ]
    cols = [c  for c in list(set(cols)) if 'None' != c ]

    filtData = data.ix[ rows, cols ]

    functions = {
        'mean'   : np.mean,
        'median' : np.median,
        'max'    : np.max,
        'min'    : np.min
    }

    # Create a list of outer groups ...
    filtList = {}
    if (postdata['gBy'] is not None) and ('None' not in postdata['gBy']):

        print 'This is : `filtData`'
        print filtData.head()
        
        for k, dfTemp in filtData.groupby(postdata['gBy']):
            dfTemp.drop(postdata['gBy'], axis=1, inplace=True)
            

            print 'This is : `dfTemp`'
            print dfTemp.head()

            # We want a further agg here ...
            if (postdata['gByI'] is not None) and ('None' not in postdata['gByI']):
                filtList[k] =  dfTemp.groupby( postdata['gByI'] ).agg(  functions[postdata['agg']] ).reset_index()  
            else:
                filtList[k] =  dfTemp 

    else:
        filtList['all'] = filtData

    for l in filtList:
        print '+----------------'
        print '|', l
        print '+----------------'

        print filtList[l].head()

    # Now we need to format the data ...
    toReturn = []

    for l in filtList:
        
        filtList[l]['x'] = filtList[l][ postdata['x'] ]
        filtList[l]['y'] = filtList[l][ postdata['y'] ]

        tempDict = dictizeDf(filtList[l][ [ 'x', 'y' ] ])
        tempDict['name'] = l
        # tempDict['type'] = 'scatter'
        # tempDict['mode'] = 'markers'
        # tempDict['xaxis'] = { 'title': postdata['x'] }
        # tempDict['yaxis'] = { 'title': postdata['y'] }

        toReturn.append( json.dumps( tempDict )   )

    toReturn = '[%s]'%( ','.join(toReturn) )
    # toReturn = toReturn.replace( postdata['x'] , 'x').replace( postdata['y'] , 'y')
    print toReturn

    # toReturn = '''[{"x":[1,2,20,10],"y":[10,15,13,17],"mode":"markers","type":"scatter"},{"x":[2,3,4,5],"y":[16,5,11,9],"mode":"lines","type":"scatter"},{"x":[1,2,3,4],"y":[12,9,15,12],"mode":"lines+markers","type":"scatter"}]'''

    return toReturn

@app.route('/data/raw', method='OPTIONS')
@enable_cors
def testFnOptions():
    return

if __name__ == '__main__':
    
    files = [os.path.join('../../data', f) for f in os.listdir('../../data') if 'resale-flat-prices-based-on-' in f ]
    data  = pd.concat(map(pd.read_csv, files))

    # Transformations:
    # data.month = data.month.astype(np.datetime64)
    data.storey_range = data.storey_range.map( tostoreyMean )
    data.resale_price = data.resale_price/100000
    # data['flat'] = data.flat_model + '-#-' + data.flat_type


    bottle.run(app)

