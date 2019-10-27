from django.shortcuts import render

def index(request):
    return render(request, 'akasaka_mitsuke_now/index.html', {
        'deptTime': '19:14',
        'destination': '荻窪',
        'note': '荻窪方面',
        'getTime': '19:10'
    })
