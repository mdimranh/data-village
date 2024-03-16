import time

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from apps.data.models import Folder


def DataView(request, *args, **kwargs):
    colors = [
        "#4B5563",
        "#E02424",
        "#9F580A",
        "#057A55",
        "#1C64F2",
        "#5850EC",
        "#7E3AF2",
        "#D61F69",
    ]
    if request.method == "GET":
        folders = Folder.objects.filter(parent__isnull=True)
        return render(
            request,
            "dashboard/data/datas.html",
            {"folders": folders, "colors": colors, "parent": True},
        )

    if request.method == "POST":
        if request.htmx:
            data = {
                "name": request.POST.get("name"),
                "premium": request.POST.get("premium") == "yes",
                "color": request.POST.get("color"),
            }
            folder = Folder(**data)
            folder.save()
            folders = Folder.objects.filter(parent__isnull=True)

            return render(
                request,
                "dashboard/data/folders.html",
                {"folders": folders, "colors": colors, "parent": True},
            )


def SubFolder(request, fid, **kwargs):
    colors = [
        "#4B5563",
        "#E02424",
        "#9F580A",
        "#057A55",
        "#1C64F2",
        "#5850EC",
        "#7E3AF2",
        "#D61F69",
    ]
    if request.method == "GET":
        folders = Folder.objects.filter(parent__id=fid)
        return render(
            request,
            "dashboard/data/datas.html",
            {"folders": folders, "colors": colors},
        )

    if request.method == "POST":
        if request.htmx:
            data = {
                "name": request.POST.get("name"),
                "premium": request.POST.get("premium") == "yes",
                "color": request.POST.get("color"),
                "parent": Folder.objects.get(id=fid),
            }
            folder = Folder(**data)
            folder.save()
            folders = Folder.objects.filter(parent__id=fid)

            return render(
                request,
                "dashboard/data/folders.html",
                {"folders": folders, "colors": colors},
            )


def DeleteFolder(request, **kwargs):
    colors = [
        "#4B5563",
        "#E02424",
        "#9F580A",
        "#057A55",
        "#1C64F2",
        "#5850EC",
        "#7E3AF2",
        "#D61F69",
    ]
    if request.method == "DELETE":
        # time.sleep(5)
        id = request.GET.get("id")
        folder = Folder.objects.filter(
            id=id
        ).first()  # Use first() to get the first object in the queryset
        if folder is None:
            return HttpResponseNotFound(
                "Folder not found"
            )  # Return 404 response if folder is not found
        else:
            folder.delete()
            if folder.parent is not None:
                folders = Folder.objects.filter(parent__id=folder.parent.id)
                return render(
                    request,
                    "dashboard/data/folders.html",
                    {"folders": folders, "colors": colors},
                )
            else:
                folders = Folder.objects.filter(parent__isnull=True)
                return render(
                    request,
                    "dashboard/data/folders.html",
                    {"folders": folders, "colors": colors, "parent": True},
                )
            return HttpResponse("Folder deleted successfully")
