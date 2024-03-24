from django.shortcuts import render


def datas(request, type):
    if type == "xlsx":
        context = {"xlsx": True}
    else:
        context = {"xlsx": False}
    return render(request, "files/viewer.html", context)


def data(request, type):
    if type == "xlsx":
        context = {"xlsx": True}
    else:
        context = {"xlsx": False}
    return render(request, "files/viewer1.html", context)
