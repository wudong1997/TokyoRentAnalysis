import requests
from bs4 import BeautifulSoup
import time

info_data = []

import csv
# 表头
labels = ['Mansion', 'Address', 'rent', 'management-cost', 'deposit', 'gratuity', 'room-type', 'area']

try:
    with open('data/itabashi.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=labels)
        writer.writeheader()
except IOError:
    print("I/O error")


# def init_dict():
#     origin_dict = {'Mansion': '', 'Address': '', 'rent': '', 'management-cost': '', 'deposit': '', 'gratuity': '',
#                    'room-type': '', 'area': ''}
#     return origin_dict


def get_all_room_link(page):
    url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13119&cb=0.0&ct=9999999&et=9999999&md=01&md=02&md=03&md=04&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&page=' + str(
        page)
    strHTML = requests.get(url)

    soup = BeautifulSoup(strHTML.text, 'html.parser')
    data = soup.find_all('div', attrs={'cassetteitem'})
    for item in data:
        # マンションの名前
        name = item.find_all('div', attrs={'class': 'cassetteitem_content-title'})[0].text
        # 住所
        address = item.find_all('li', attrs={'class': 'cassetteitem_detail-col1'})[0].text

        room_info = item.find_all('tr', attrs={'class': 'js-cassette_link'})
        for each in room_info:
            # 家賃
            rent = each.find_all('span', attrs={'class': 'cassetteitem_other-emphasis ui-text--bold'})[0].text
            # 管理費
            management_cost = \
                each.find_all('span', attrs={'class': 'cassetteitem_price cassetteitem_price--administration'})[0].text
            # 敷金
            deposit = each.find_all('span', attrs={'class': 'cassetteitem_price cassetteitem_price--deposit'})[0].text
            # 礼金
            gratuity = each.find_all('span', attrs={'class': 'cassetteitem_price cassetteitem_price--gratuity'})[0].text
            # 間取りタイプ
            room_type = each.find_all('span', attrs={'class': 'cassetteitem_madori'})[0].text
            # 面積
            area = each.find_all('span', attrs={'class': 'cassetteitem_menseki'})[0].text
            info_set = {'Mansion': name,
                        'Address': address,
                        'rent': rent,
                        'management-cost': management_cost,
                        'deposit': deposit,
                        'gratuity': gratuity,
                        'room-type': room_type,
                        'area': area
                        }
            try:
                with open('data/itabashi.csv', 'a', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=labels)
                    writer.writerow(info_set)
            except IOError:
                print("I/O error")


def data_modify(file_name):
    """
    将爬取的数据进行整理，提取其中的数字，如：8万円->80000.0; 填充nan值
    :param file_name: 文件名
    :return: dataFrame
    """
    df = pd.read_csv(file_name, header=0)
    df['rent'] = df['rent'].str.extract(r'(\d+\.?\d*)', expand=True).astype(float).multiply(10000)
    df['area'] = df['area'].str.extract(r'(\d+\.?\d*)', expand=True).astype(float).fillna(0)
    df['management-cost'] = df['management-cost'].str.extract(r'(\d+\.?\d*)', expand=True).astype(float).fillna(0)
    df['deposit'] = df['deposit'].str.extract(r'(\d+\.?\d*)', expand=True).astype(float).multiply(10000).fillna(0)
    df['gratuity'] = df['gratuity'].str.extract(r'(\d+\.?\d*)', expand=True).astype(float).multiply(10000).fillna(0)

    return df


get_all_room_link(PAGE)
