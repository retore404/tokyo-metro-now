from django.shortcuts import render
from django.conf import settings

import requests

def index(request):
    # settings.pyに設定したAPIキーの読み込み
    apiKey = getattr(settings, "API_KEY", None)
    
    # 丸ノ内線走行中全列車の走行位置情報を取得
    trainUrlRoot = 'https://api.tokyometroapp.jp/api/v2/datapoints'
    
    response = requests.get(
        trainUrlRoot,
        params = {'rdf:type': 'odpt:Train',
                  'acl:consumerKey': apiKey,
                  'odpt:railway': 'odpt.Railway:TokyoMetro.Marunouchi'}
    )
    
    # レスポンスから荻窪方面・方南町方面（A線）の列車を抜き出し
    data = response.json()
    data = [train for train in data if train['odpt:railDirection'] == 'odpt.RailDirection:TokyoMetro.Ogikubo' or train['odpt:railDirection'] == 'odpt.RailDirection:TokyoMetro.Honancho']
    

    for t in data:
        print(t)

    return render(request, 'akasaka_mitsuke_now/index.html', {
        'deptTime': '19:14',
        'destination': '荻窪',
        'note': '荻窪方面',
        'getTime': '19:10'
    })
