from numpy import nan
import requests
import pandas as pd

KEY = ''


def get_coord(address, API_KEY=KEY):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address},+JP&&key={API_KEY}'
    r = requests.get(url)
    ro = r.json()

    lat = ''
    lng = ''
    formatted_address = ''
    try:
        result = ro.get('results')[0]
        coordination = result.get('geometry').get('location')
        lat = coordination.get('lat')
        lng = coordination.get('lng')

        formatted_address = result.get('formatted_address')
    except IndexError as nodata:
        coordination = 'None'

    return lat, lng, formatted_address


def location(file):
    df = pd.read_csv(file)

    lat_arr = []
    lng_arr = []
    fa_arr = []
    for item in df['full_address']:
        lat, lng, fa = get_coord(item)
        lat_arr.append(lat)
        lng_arr.append(lng)
        fa_arr.append(fa)

    df['latitude'] = lat_arr
    df['longitude'] = lng_arr
    df['full_address'] = fa_arr

    return df

df = location('READFILENAME')
df.to_csv('{}.csv'.format('WRITEFILENAME'), encoding='utf-8', index=0)
