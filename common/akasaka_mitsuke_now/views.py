from django.shortcuts import render
from django.conf import settings

def index(request):
    print(getattr(settings, "API_KEY", None))
    return render(request, 'akasaka_mitsuke_now/index.html', {
        'deptTime': '19:14',
        'destination': '荻窪',
        'note': '荻窪方面',
        'getTime': '19:10'
    })
