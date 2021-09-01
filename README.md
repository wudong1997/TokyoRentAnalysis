# TokyoRentAnalysis
东京23区单身公寓（1K、1DK）月租金数据爬取、处理、分析、可视化

## 数据源
<div>
房租数: SUUMO（スーモ）- 日本最大級の不動産サイトSUUMO https://suumo.jp/kanto/  <div>
位置信息：Google Map API https://developers.google.com/maps <div>
地理数据：日本国土地理院　https://www.gsi.go.jp/ <div>

## Google Map API的使用
  <div>
  主页：https://developers.google.com/maps<div>
  文档：https://developers.google.com/maps/documentation<div>
  此次只用了Geocoding API，因此简单介绍一下这部分的使用
    
  ### 地理编码（Geocoding）
  <div>
  地理编码是将地址转换为地理坐标的过程<div>
  如：Kita-ayase Sta., 2-chōme-6 Yanaka, Adachi City, Tokyo 120-0006, Japan -> 35.7770135,139.8321012
    
  ### Geocoding API request method
  <div>
  可以使用https://maps.googleapis.com/maps/api/geocode/outputFormat?parameters 进行数据访问<div>
  outputFormat：输出格式，json或者xml
    
  ```
  API_KEY = 'aaaaaaaaaaaaabbbbbbbbbb' 
  url = f'https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&&key={API_KEY}'
  r = requests.get(url)
  ro = r.json()
  ```
  将ro作为结果输出(简化）<div>
  
  ```
  {
   "results" : [
      {
         "address_components" : [
            {
               "long_name" : "1600",
               "short_name" : "1600",
               "types" : [ "street_number" ]
            },
            {
               "long_name" : "Amphitheatre Pkwy",
               "short_name" : "Amphitheatre Pkwy",
               "types" : [ "route" ]
            },
            ...
         ],
         "formatted_address" : "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
         "geometry" : {
            "location" : {
               "lat" : 37.4224764,
               "lng" : -122.0842499
            },
         },
         "place_id" : "ChIJ2eUgeAK6j4ARbn5u_wAGqWA",
         "plus_code": {
            "compound_code": "CWC8+W5 Mountain View, California, United States",
            "global_code": "849VCWC8+W5"
         },
      }
   ],
   "status" : "OK"
  }
  ```
  之后可通过读取json的方式读取相关信息
  ```
  coordination = ro.get('geometry').get('location')
  lat = coordination.get('lat')
  lng = coordination.get('lng')
  ```
 
  ## 爬虫
  如图所示为suumo的信息界面，以公寓楼为单位，进行读取
  ![image](https://github.com/wudong1997/TokyoRentAnalysis/blob/main/image/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE(61).png)<div>
  需要的信息包括：
  ```
    {'Mansion': 'ＪＲ山手線 秋葉原駅 地下1地上21階建 築16年',
     'Address': '東京都千代田区神田練塀町',
     'rent': '26万円',
     'management-cost': '15000円',
     'deposit': '26万円',
     'gratuity': '26万円',
     'room_type': '2LDK',
     'area': '66.92m2',
     'distance': 'ＪＲ山手線/秋葉原駅 歩4分',
     'built_year': '築16年',
     'floors': '9階'
     }
  ```
