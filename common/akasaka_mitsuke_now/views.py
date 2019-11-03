from django.shortcuts import render
from django.conf import settings

import requests

def index(request):
    # settings.pyに設定したAPIキーの読み込み
    apiKey = getattr(settings, "API_KEY", None)    
    urlRoot = 'https://api.tokyometroapp.jp/api/v2/datapoints'

    # 赤坂見附・A線の時刻表を取得
    response = requests.get(
        urlRoot,
        params = {'rdf:type': 'odpt:StationTimetable',
                  'acl:consumerKey': apiKey,
                  'odpt:railway': 'odpt.Railway:TokyoMetro.Marunouchi',
                  'odpt:station': 'odpt.Station:TokyoMetro.Marunouchi.AkasakaMitsuke',
                  'odpt:railDirection': 'odpt.RailDirection:TokyoMetro.Ogikubo'}
    )

    data = response.json()

    for d in data:
        print(d)

    

    return render(request, 'akasaka_mitsuke_now/index.html', {
        'deptTime': '19:14',
        'destination': '荻窪',
        'note': '荻窪方面',
        'getTime': '19:10'
    })
