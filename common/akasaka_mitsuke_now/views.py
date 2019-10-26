from django.shortcuts import render

def index(request):
    return render(request, 'akasaka_mitsuke_now/index.html', {
        'val': 'test',
    })
