from django.shortcuts import render
from django.conf import settings

import requests

def index(request):
    # settings.pyに設定したAPIキーの読み込み
    apiKey = getattr(settings, "API_KEY", None)    
    urlRoot = 'https://api.tokyometroapp.jp/api/v2/datapoints'

    # 丸ノ内線走行中全列車の走行位置情報を取得
    responseTrains = requests.get(
        urlRoot,
        params = {'rdf:type': 'odpt:Train',
                  'acl:consumerKey': apiKey,
                  'odpt:railway': 'odpt.Railway:TokyoMetro.Marunouchi'}
    )
    
    # レスポンスから荻窪方面・方南町方面（A線）の列車を抜き出し
    trains = responseTrains.json()
    date = trains[0]['dc:date'] # 取得日時
    trainsA = [train for train in trains if train['odpt:railDirection'] == 'odpt.RailDirection:TokyoMetro.Ogikubo' or train['odpt:railDirection'] == 'odpt.RailDirection:TokyoMetro.Honancho']

    # A線の走行列車から赤坂見附停車中or接近中の列車を抜き出し
    trainsTarget = [train for train in trainsA 
    if (train["odpt:toStation"] == None and train["odpt:fromStation"] == "odpt.Station:TokyoMetro.Marunouchi.AkasakaMitsuke")  # 赤坂見附停車中
    or train["odpt:fromStation"] == "odpt.Station:TokyoMetro.Marunouchi.KokkaiGijidomae" # 国会議事堂前停車中 or 発車
    or train["odpt:fromStation"] == "odpt.Station:TokyoMetro.Marunouchi.Kasumigaseki" # 霞ケ関停車中or発車
    or train["odpt:fromStation"] == "odpt.Station:TokyoMetro.Marunouchi.Ginza" # 銀座
    or train["odpt:fromStation"] == "odpt.Station:TokyoMetro.Marunouchi.Tokyo" # 東京
    or train["odpt:fromStation"] == "odpt.Station:TokyoMetro.Marunouchi.Otemachi" # 大手町
    or train["odpt:fromStation"] == "odpt.Station:TokyoMetro.Marunouchi.Awajicho" # 淡路町
    or train["odpt:fromStation"] == "odpt.Station:TokyoMetro.Marunouchi.Ochanomizu" # 御茶ノ水
    or train["odpt:fromStation"] == "odpt.Station:TokyoMetro.Marunouchi.HongoSanchome" # 本郷三丁目
    or train["odpt:fromStation"] == "odpt.Station:TokyoMetro.Marunouchi.Korakuen" # 後楽園
    or train["odpt:fromStation"] == "odpt.Station:TokyoMetro.Marunouchi.Myogadani" # 茗荷谷
    or (train["odpt:fromStation"] == "odpt.Station:TokyoMetro.Marunouchi.ShinOtsuka" and train["odpt:terminalStation"] != "odpt.Station:TokyoMetro.Marunouchi.Myogadani") # 新大塚
    or (train["odpt:fromStation"] == "odpt.Station:TokyoMetro.Marunouchi.Ikebukuro" and train["odpt:terminalStation"] != "odpt.Station:TokyoMetro.Marunouchi.Myogadani") # 池袋 茗荷谷行きは除外
    ]

    # 丸ノ内線の列車時刻表を取得
    responseTimeTable = requests.get(
        urlRoot,
        params = {
            'rdf:type' : 'odpt:TrainTimetable',
            'acl:consumerKey': apiKey,
            'odpt:railway' : 'odpt.Railway:TokyoMetro.Marunouchi'
        }
    )
    timeTable = responseTimeTable.json()

    # A線走行中で赤坂見附をこれから発車する列車の一覧格納リスト（出力用）
    trainsValid = [] # ['赤坂見附発車時刻', '行き先', '遅延']

    

    





    return render(request, 'akasaka_mitsuke_now/index.html', {
        'deptTime': '19:14',
        'destination': '荻窪',
        'note': '荻窪方面',
        'getTime': '19:10'
    })

def getAkasakaMitsukeDeptTime(trainNumber):
    pass
