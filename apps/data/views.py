from django.shortcuts import render


def datas(request, type):
    if type == "xlsx":
        context = {
            "xlsx": True
        }
    else:
        context = {"xlsx": False}
    return render(request, 'files/viewer.html', context)