from django.shortcuts import render


def DataView(request, *args, **kwargs):
    return render(request, 'dashboard/data/datas.html')