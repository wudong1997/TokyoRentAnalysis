from numpy import nan
import requests
import pandas as pd

KEY = 'AIzaSyByBXvK0ASTyfdDsOHiuayBIMGbvwirfQE'


def get_coord(address, API_KEY=KEY):
    address = address
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


# fl = ['./p_data/n_itabashi.csv', './p_data/n_kita.csv', './p_data/n_meguro.csv', './p_data/n_nakano.csv',
#       './p_data/n_nerimaku.csv', './p_data/n_oda.csv', './p_data/n_suginami.csv', './p_data/n_toshima.csv']
#
# aim = ['itabashi_loc', 'kita_loc', 'meguro_loc', 'nakano_loc',
#       'nerimaku_loc', 'oda_loc', 'suginami_loc', 'toshima_loc']
#
# for i in range(len(fl)):
#     df = location(fl[i])
#     df.to_csv('{}.csv'.format(aim[i]), encoding='utf-8', index=0)
#     print(i)


df = location('./p_data/n_sedagaya.csv')
df.to_csv('{}.csv'.format('sedagaya.loc'), encoding='utf-8', index=0)
