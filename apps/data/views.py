from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.data.models import File, Folder


def datas(request, id=None):
    context = {}
    if id:
        folder = Folder.objects.filter(id=id).first()
        folders = Folder.objects.filter(parent__id=id)
        context["folders"] = folders
        files = File.objects.filter(folder__id=id)
        context["files"] = files
        context["sequence"] = folder.sequence if folder else None
    else:
        folders = Folder.objects.filter(parent__isnull=True)
        context["folders"] = folders
        context["parent"] = True
    if request.htmx:
        return render(
            request,
            "data/folders.html",
            context,
        )
    return render(
        request,
        "data/datas.html",
        context,
    )
    # return render(request, "data/datas.html")


def data(request, type):
    if type == "xlsx":
        context = {"xlsx": True}
    else:
        context = {"xlsx": False}
    return render(request, "files/viewer1.html", context)
