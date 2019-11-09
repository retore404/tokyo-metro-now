from django.shortcuts import render
from django.conf import settings

import requests
import datetime

def index(request):

    # settings.pyに設定したAPIキーの読み込み
    apiKey = getattr(settings, "SECRET_KEY", None)    
    urlRoot = 'https://api.tokyometroapp.jp/api/v2/datapoints'

    # 現在時刻の取得
    currentTime = datetime.datetime.now()
    currentHour = ('0' + str(currentTime.hour))[-2:]
    currentMinute = ('0' + str(currentTime.minute))[-2:]

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

    nextTwoTrains = getNextTwoTrains(data[0]['odpt:weekdays'])

    # 結果表示内容格納用リスト
    output = [['--:--', '----', '----'], ['--:--', '----', '----']]

    for i in range(len(nextTwoTrains)):
        output[i][0] = nextTwoTrains[i]['odpt:departureTime']
        output[i][1] = getStationName(nextTwoTrains[i]['odpt:destinationStation'])
        if nextTwoTrains[i]['odpt:destinationStation'] == True:
            output[i][2] = '本日の最終列車です．' 
        else:
            output[i][2] = '　　　　　'               

    return render(request, 'akasaka_mitsuke_now/index.html', {
        'deptTimeFirst': output[0][0],
        'destinationFirst': output[0][1],
        'noteFirst': output[0][2],
        'deptTimeSecond': output[1][0],
        'destinationSecond': output[1][1],
        'noteSecond': output[1][2],
        'currentTime': str(currentHour) + ':' +str(currentMinute)
    })

def getStationName(odptStr):
    if odptStr == 'odpt.Station:TokyoMetro.Marunouchi.Shinjuku':
        return '新宿'
    elif odptStr == 'odpt.Station:TokyoMetro.Marunouchi.Ogikubo':
        return '荻窪'
    elif odptStr == 'odpt.Station:TokyoMetro.MarunouchiBranch.Honancho':
        return '方南町'
    elif odptStr == 'odpt.Station:TokyoMetro.MarunouchiBranch.NakanoFujimicho':
        return '中野富士見町'
    elif odptStr == 'odpt.Station:TokyoMetro.Marunouchi.NakanoSakaue':
        return '中野坂上'
    else:
        return odptStr

# データ取得時以降の2本分のStationTimeTableObjectを返す
def getNextTwoTrains(stationTimetableObjectArray):
    # 現在時刻の取得
    currentTime = datetime.datetime.now()
    
    # 日付変更後の比較のための変換
    currentHH = currentTime.hour
    currentMM = currentTime.minute
    
    # 時刻が0:00～3:59時の場合，+24し24時～27時として計算する．
    if currentHH <= 3:
        tmpCurrentHH = currentHH + 24
    else:
        tmpCurrentHH = currentHH

    count = 0
    result = []
    for timeRow in stationTimetableObjectArray:
        timeRowHH = int(timeRow['odpt:departureTime'][0:2]) #StationTimeTableObjectの出発時間の時部分2桁
        timeRowMM = int(timeRow['odpt:departureTime'][-2:]) #StationTimeTableObjectの出発時間の分部分2桁

        # 時刻が0:00～3:59時の場合，+24し24時～27時として計算する．
        # 時刻が0:00～3:59時の場合，+24し24時～27時として計算する．
        if timeRowHH <= 3:
            tmpTimeRowHH = timeRowHH + 24
        else:
            tmpTimeRowHH = timeRowHH
        
        # 現在時のHHと参照中の時刻表行のHHを比較
        if tmpCurrentHH > tmpTimeRowHH: # 現在時のHHのほうが進んでいる（＝現在時から見て過去の時刻表行を見ている）
            pass
        elif currentMM > timeRowMM: # 現在時のHHのほうが進んでおらず（HHだけで見ると未来の時刻を見ていて），かつ現在時MMのほうが時刻表行MMより大きい（＝現在時から見て過去の時刻表行を見ている）
            pass
        else: # 未来の時刻表を見ている
            break
        
        # 行カウント用変数を1増やす
        count += 1
        
    try:
        result.append(stationTimetableObjectArray[count])
        result.append(stationTimetableObjectArray[count+1])
    except IndexError:
        pass

    return result