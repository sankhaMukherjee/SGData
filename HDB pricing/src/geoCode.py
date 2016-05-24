import googlemaps 
import pandas as pd 
gmaps = googlemaps.Client(key='AIzaSyDlOvwsHFMsPSf9B59akZfWp0kehmamftQ')

def getAddressString(address):
    '''
        Given a Street Address, this is going to 
        convert the address into a latitude, longitude
        and a full address
    '''

    success, result = False, None

    try:
        value = gmaps.geocode(address)

        result = {}
        result['address'] = address
        result['full address'] = value[0]['formatted_address']
        result.update( value[0]['geometry']['location'] )

        success = True
    except:

        pass

    return success, result

def collectCodes(addressList):
    '''
        We want some way of caching results here. So we
        are not going to go through the entire database 
        and will only ask for values which are not present.

        This way we omly collect data that we have not catched ...
    '''

    allAddresses = []

    N = len(addressList)
    for i, address in enumerate(addressList):
        print i+1, 'of', N, ':', address
        success, result = getAddressString(address)

        if not success: break

        print result['full address']
        allAddresses.append( result )

    return allAddresses

if __name__ == '__main__':

    data = pd.read_csv('../data/relaseData.csv')
    prevAddresses = pd.read_csv('../data/addressData.csv')

    addressList  = list(data['address'].unique())
    addressList  = [a for a in addressList if a not in list(prevAddresses.address)]
    allAddresses = pd.DataFrame(collectCodes( addressList ))

    allAddresses = pd.concat([ prevAddresses, allAddresses ])

    allAddresses.to_csv('../data/addressData.csv', index=False)


    print allAddresses

    print 'done'


